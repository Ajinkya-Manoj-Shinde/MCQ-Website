from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_test/', views.create_test, name='create_test'),
    path('create_test/<int:test_id>/questions/', views.create_questions, name='create_questions'),
    path('question/<int:question_id>/choices/', views.edit_choices, name='edit_choices'),
    path('test/<int:test_id>/student_info/', views.student_info, name='student_info'),
    path('test/<int:test_id>/take/', views.take_test, name='take_test'),
    path('test_attempt/<int:test_attempt_id>/submit/', views.submit_test, name='submit_test'),
    path('test/<int:test_id>/results/', views.results, name='results'),
    path('login/', views.teacher_login, name='login'),
    path('logout/', views.teacher_logout, name='logout'),
]
