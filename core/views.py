from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Profile
from .models import LiveQuiz, Question, Answer, Doubt, StudentResponse, Discussion,StudentProfile, TeacherProfile
from .forms import LiveQuizForm, QuestionForm, AnswerForm, DoubtForm, DiscussionForm,StudentProfileForm, TeacherProfileForm
from django.db.models import Avg, Count, Sum, F, FloatField, ExpressionWrapper, Q, Case, When, F
from django.db.models.functions import Coalesce
from django.forms import modelformset_factory
from django.utils import timezone



# 🔹 SIGNUP VIEW
from django.db import IntegrityError
from .models import Profile

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        user_type = request.POST.get('user_type')
        print("User type received:", user_type)

        if user_type:
            user_type = user_type.capitalize().strip()

        if form.is_valid() and user_type in ['Student', 'Teacher']:
            try:
                user = form.save()
                # ✅ Check if profile already exists
                profile, created = Profile.objects.get_or_create(user=user)
                profile.user_type = user_type
                profile.save()

                login(request, user)
                print("✅ Registration successful. Redirecting to /success/")
                return redirect('success')
            except IntegrityError as e:
                print("❌ IntegrityError:", str(e))
                form.add_error(None, "A problem occurred during profile creation.")
        else:
            print("❌ Form is invalid or user_type is incorrect.")
            print(form.errors)

    else:
        form = UserCreationForm()

    return render(request, 'core/signup.html', {'form': form})




# 🔹 LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            try:
                profile = Profile.objects.get(user=user)
                user_type = profile.user_type.lower()

                if user_type == 'student':
                    return redirect('student_dashboard')
                elif user_type == 'teacher':
                    return redirect('teacher_dashboard')
                else:
                    return redirect('unknown_role')
            except Profile.DoesNotExist:
                return redirect('unknown_role')
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


# 🔹 SUCCESS PAGE
def success_view(request):
    return render(request, 'core/success.html')


# 🔹 DASHBOARDS
@login_required
def student_dashboard_view(request):
    return render(request, 'core/student_dashboard.html')

@login_required
def teacher_dashboard_view(request):
    return render(request, 'core/teacher_dashboard.html')


@login_required
def unknown_role_view(request):
    return render(request, 'core/unknown_role.html')



@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = LiveQuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = LiveQuizForm()
    return render(request, 'core/create_quiz.html', {'form': form})


@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(LiveQuiz, id=quiz_id)
    AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=4)

    if request.method == 'POST':
        q_form = QuestionForm(request.POST)
        a_formset = AnswerFormSet(request.POST, queryset=Answer.objects.none())

        if q_form.is_valid() and a_formset.is_valid():
            question = q_form.save(commit=False)
            question.quiz = quiz
            question.save()

            for form in a_formset:
                answer = form.save(commit=False)
                answer.question = question
                answer.save()

            return redirect('add_question', quiz_id=quiz.id)
    else:
        q_form = QuestionForm()
        a_formset = AnswerFormSet(queryset=Answer.objects.none())

    return render(request, 'core/add_question.html', {
        'quiz': quiz,
        'q_form': q_form,
        'a_formset': a_formset
    })


@login_required
def teacher_quizzes(request):
    quizzes = LiveQuiz.objects.filter(created_by=request.user)
    return render(request, 'core/teacher_quizzes.html', {'quizzes': quizzes})

@login_required
def launch_quiz(request, quiz_id):
    quiz = get_object_or_404(LiveQuiz, id=quiz_id)
    quiz.is_active = True
    quiz.save()
    return redirect('teacher_quizzes')

@login_required
def submit_doubt(request):
    if request.method == 'POST':
        form = DoubtForm(request.POST)
        if form.is_valid():
            doubt = form.save(commit=False)
            doubt.student = request.user
            doubt.save()
            return redirect('student_dashboard')
    else:
        form = DoubtForm()
    return render(request, 'core/submit_doubt.html', {'form': form})


@login_required
def manage_doubts(request):
    doubts = Doubt.objects.all().order_by('-created_at')
    return render(request, 'core/manage_doubts.html', {'doubts': doubts})

@login_required
def resolve_doubt(request, doubt_id):
    doubt = get_object_or_404(Doubt, id=doubt_id)
    doubt.is_resolved = True
    doubt.save()
    return redirect('manage_doubts')

@login_required
def reply_to_doubt(request, doubt_id):
    doubt = get_object_or_404(Doubt, id=doubt_id)

    if request.method == 'POST':
        reply = request.POST.get('reply')
        doubt.reply = reply
        doubt.is_resolved = True
        doubt.save()
        return redirect('manage_doubts')

    return render(request, 'core/reply_doubt.html', {'doubt': doubt})

@login_required
def my_doubts(request):
    doubts = Doubt.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'core/my_doubts.html', {'doubts': doubts})


@login_required
def available_quizzes(request):
    quizzes = LiveQuiz.objects.filter(is_active=True)
    return render(request, 'core/available_quizzes.html', {'quizzes': quizzes})

@login_required
def attempt_quiz(request, quiz_id):
    quiz = get_object_or_404(LiveQuiz, id=quiz_id, is_active=True)
    questions = Question.objects.filter(quiz=quiz).prefetch_related('answers')

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for question in questions:
            selected_id = request.POST.get(f'question_{question.id}')
            if selected_id:
                selected_answer = Answer.objects.get(id=selected_id)
                is_correct = selected_answer.is_correct

                # Store response
                StudentResponse.objects.create(
                    student=request.user,
                    quiz=quiz,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=is_correct
                )

                if is_correct:
                    score += 1

        # Send score to results page
        return render(request, 'core/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total': total
        })

    return render(request, 'core/attempt_quiz.html', {'quiz': quiz, 'questions': questions})



@login_required
def monitor_engagement(request):
    from django.db.models import Count, Sum, F, FloatField, ExpressionWrapper
    from django.contrib.auth.models import User
    from django.db.models.functions import Cast

    # Get total answers and correct ones per student
    stats = (
        StudentResponse.objects
        .values('student__username', 'student')
        .annotate(
            total_answers=Count('id'),
            correct_answers=Sum('is_correct'),
            quizzes_attempted=Count('quiz', distinct=True),
            accuracy=ExpressionWrapper(
                100.0 * Sum('is_correct') / Count('id'),
                output_field=FloatField()
            )
        )
        .order_by('-accuracy')
    )

    return render(request, 'core/monitor_engagement.html', {'engagement': stats})


@login_required
def student_dashboard(request):
    student = request.user

    responses = StudentResponse.objects.filter(student=student)
    quiz_ids = responses.values_list('question__quiz_id', flat=True).distinct()
    quizzes_attempted = quiz_ids.count()

    total_attempts = responses.count()
    correct_answers = responses.filter(is_correct=True).count()

    accuracy = round((correct_answers / total_attempts) * 100, 2) if total_attempts > 0 else 0

    context = {
        'quizzes_attempted': quizzes_attempted,
        'total_attempts': total_attempts,
        'correct_answers': correct_answers,
        'accuracy': accuracy,
    }

    return render(request, 'core/student_dashboard.html', context)


@login_required
def discussion_view(request):
    discussions = Discussion.objects.all().order_by('-posted_at')
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('discussion')
    else:
        form = DiscussionForm()
    return render(request, 'core/discussion.html', {'form': form, 'discussions': discussions})

@login_required
def videos_view(request):
    return render(request, 'core/videos.html')


def home(request):
    return render(request,'core/home.html',{})


@login_required
def edit_profile(request):
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile(user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def edit_teacher_profile(request):
    teacher, created = TeacherProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')  # or any success page
    else:
        form = TeacherProfileForm(instance=teacher)
    return render(request, 'core/edit_teacher_profile.html', {'form': form})














# @login_required
# def view_received_doubts(request):
#     doubts = request.user.doubts_received.all()
#     return render(request, 'core/received_doubts.html', {'doubts': doubts})
