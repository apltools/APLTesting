from django.contrib import admin
from .models import CourseSite, Test, Student, Question, Attempt

admin.site.register(CourseSite)
admin.site.register(Test)
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Attempt)
