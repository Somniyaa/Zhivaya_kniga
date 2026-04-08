from django.urls import path
from . import views

urlpatterns = [
    path('', views.quizzes_list, name='quizzes_list'),
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
]