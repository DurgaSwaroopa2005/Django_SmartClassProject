
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import LiveQuiz, Question, Answer, Doubt, Discussion


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
        fields = ['question']

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your comment...'})
        }

