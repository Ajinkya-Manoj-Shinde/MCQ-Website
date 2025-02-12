from django.contrib import admin
from .models import Test, Question, Choice, Student, TestAttempt, Answer

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Student)
admin.site.register(TestAttempt)
admin.site.register(Answer)
# Register your models here.
