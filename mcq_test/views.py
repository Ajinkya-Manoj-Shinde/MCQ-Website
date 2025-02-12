
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.utils import timezone
from .models import Test, Question, Choice, Student, TestAttempt, Answer
from .forms import TestForm, QuestionForm, ChoiceForm, StudentInfoForm

def home(request):
    tests = Test.objects.all()
    return render(request, 'mcq_test/home.html', {'tests': tests})

@login_required
def create_test(request):
    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            test = test_form.save(commit=False)
            test.created_by = request.user
            test.save()
            return redirect('create_questions', test_id=test.id) # Redirect to add questions
    else:
        test_form = TestForm()
    return render(request, 'mcq_test/create_test.html', {'test_form': test_form})

@login_required
def create_questions(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.test = test
            question.save()

            #Create 4 choices after the question saved
            for i in range(4):
                choice = Choice(question=question)
                choice.save()
            return redirect('edit_choices', question_id=question.id) # Redirect to add questions
    else:
        question_form = QuestionForm()
    return render(request, 'mcq_test/create_questions.html', {'question_form': question_form, 'test': test})

@login_required
def edit_choices(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    choices = Choice.objects.filter(question=question)

    if request.method == 'POST':
        choice_id = request.POST.get('choice_id')
        text = request.POST.get('text')
        is_correct = request.POST.get('is_correct') == 'true'
        try:
            choice = Choice.objects.get(pk=choice_id)
            choice.text = text
            choice.is_correct = is_correct
            choice.save()
            return redirect('edit_choices', question_id=question_id)
        except Choice.DoesNotExist:
            return HttpResponse("Choice not found", status=404)

    return render(request, 'mcq_test/edit_choices.html', {'question': question, 'choices': choices})

def student_info(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    if request.method == 'POST':
        student_form = StudentInfoForm(request.POST)
        if student_form.is_valid():
            student = student_form.save()
            # Store student ID in session to track them during the test
            request.session['student_id'] = student.id
            request.session['test_id'] = test.id
            return redirect('take_test', test_id=test.id)
    else:
        student_form = StudentInfoForm()
    return render(request, 'mcq_test/student_info.html', {'student_form': student_form, 'test': test})

def take_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_info', test_id=test_id)  # Redirect to student info form if not in session

    student = get_object_or_404(Student, pk=student_id)
    questions = test.questions.all()
    test_attempt, created = TestAttempt.objects.get_or_create(test=test, student=student) # Check if the student already attempted the test or create

    if request.method == 'POST':
        for question in questions:
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                try:
                    choice = Choice.objects.get(pk=choice_id)
                    answer = Answer(test_attempt=test_attempt, question=question, choice=choice)
                    answer.save()
                except Choice.DoesNotExist:
                    pass # Handle if the choice doesn't exist (error)
            else:
              answer = Answer(test_attempt=test_attempt, question=question)
              answer.save()

        test_attempt.end_time = timezone.now()
        test_attempt.save()

        return redirect('submit_test', test_attempt_id=test_attempt.id)

    return render(request, 'mcq_test/take_test.html', {'test': test, 'questions': questions, 'student':student, 'test_attempt': test_attempt})

def submit_test(request, test_attempt_id):
    test_attempt = get_object_or_404(TestAttempt, pk=test_attempt_id)
    correct_answers = 0
    for answer in test_attempt.answers.all():
        if answer.choice and answer.choice.is_correct:
            correct_answers += 1

    test_attempt.score = correct_answers
    test_attempt.save()

    # Clear the student_id from the session
    if 'student_id' in request.session:
      del request.session['student_id']
    return render(request, 'mcq_test/submit_test.html', {'test_attempt': test_attempt, 'correct_answers': correct_answers})

@login_required
def results(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    test_attempts = TestAttempt.objects.filter(test=test).order_by('-score')
    return render(request, 'mcq_test/results.html', {'test': test, 'test_attempts': test_attempts})

def teacher_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the teacher's dashboard
            else:
                return HttpResponse("Invalid login details supplied.")
        else:
            return HttpResponse("Invalid login details supplied.")
    form = AuthenticationForm()
    return render(request = request,
                  template_name = "mcq_test/login.html",
                  context={"form":form})

@login_required
def teacher_logout(request):
    logout(request)
    return redirect("home")  # Redirect to the home page after logout
