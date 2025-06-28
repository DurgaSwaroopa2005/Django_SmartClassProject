
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import videos_view, edit_profile

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('success/', views.success_view, name='success'),

    # Dashboards
    path('student/dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('unknown/', views.unknown_role_view, name='unknown_role'),

    # Logout
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    #teacher_quiz
    path('teacher/quizzes/', views.teacher_quizzes, name='teacher_quizzes'),
path('teacher/quiz/create/', views.create_quiz, name='create_quiz'),
path('teacher/quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
path('teacher/quiz/<int:quiz_id>/launch/', views.launch_quiz, name='launch_quiz'),

path('student/submit-doubt/', views.submit_doubt, name='submit_doubt'),
path('teacher/manage-doubts/', views.manage_doubts, name='manage_doubts'),
path('teacher/resolve-doubt/<int:doubt_id>/', views.resolve_doubt, name='resolve_doubt'),
path('teacher/reply-doubt/<int:doubt_id>/', views.reply_to_doubt, name='reply_doubt'),
path('student/my-doubts/', views.my_doubts, name='my_doubts'),
path('student/quizzes/', views.available_quizzes, name='available_quizzes'),
path('student/quiz/<int:quiz_id>/', views.attempt_quiz, name='attempt_quiz'),
path('teacher/engagement/', views.monitor_engagement, name='monitor_engagement'),
path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
path('discussion/', views.discussion_view, name='discussion'),
path('videos/', videos_view, name='videos'),
path('home/', views.home, name='home'),
path('edit-profile/', edit_profile, name='edit_profile'),

]