from django import forms
from .models import Test, Question, Choice, Student

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'time_limit']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

class StudentInfoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'enrollment_number', 'email']
