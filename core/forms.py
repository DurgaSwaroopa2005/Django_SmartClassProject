
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import LiveQuiz, Question, Answer, Doubt, Discussion, StudentProfile,TeacherProfile


class CustomSignupForm(UserCreationForm):
    USER_TYPES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')

class LiveQuizForm(forms.ModelForm):
    class Meta:
        model = LiveQuiz
        fields = ['title']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your question'})
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3})
        }

class DoubtForm(forms.ModelForm):
    class Meta:
        model = Doubt
        fields = ['teacher', 'question']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show only teachers
        self.fields['teacher'].queryset = User.objects.filter(is_staff=True)
        self.fields['teacher'].label = "Send To (Teacher)"
        self.fields['question'].widget = forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your doubt here...'})

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your comment...'})
        } 



class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'branch', 'year', 'phone_number', 'profile_pic']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['full_name', 'subject', 'bio', 'profile_pic']
