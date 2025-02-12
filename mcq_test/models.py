
# Create your models here.
from django.db import models
from django.contrib.auth.models import User  # Import Django's built-in User model

class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Teacher who created the test
    created_at = models.DateTimeField(auto_now_add=True)
    time_limit = models.IntegerField(default=60)  # Time limit in minutes

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text[:50]  # Show first 50 characters


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Student(models.Model):
    name = models.CharField(max_length=255)
    enrollment_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

class TestAttempt(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)  #When student submit the test
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.name} - {self.test.title}"

class Answer(models.Model):
    test_attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)  # Student's chosen answer
    def __str__(self):
        return f"Answer to Question {self.question.id} in Test Attempt {self.test_attempt.id}"
