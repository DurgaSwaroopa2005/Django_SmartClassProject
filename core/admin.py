from django.contrib import admin

from .models import Profile

# admin.site.register(Profile)

from .models import (
    Profile, LiveQuiz, Question, Answer, Doubt, StudentResponse,
    Discussion, StudentProfile, TeacherProfile
)

# Register your models here.
admin.site.register(Profile)
admin.site.register(LiveQuiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Doubt)
admin.site.register(StudentResponse)
admin.site.register(Discussion)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
