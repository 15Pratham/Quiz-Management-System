from django.urls import path
from .views import available_quizzes,join_quiz,add_question,add_option
from . import views

urlpatterns = [
    path('create/', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('add-option/', views.add_option, name='add_option'),
    path('publish/<int:quiz_id>/', views.publish_quiz, name='publish_quiz'),
    path('view-attempts/', views.view_attempts, name='view_attempts'),
    path('download-results/', views.download_pdf, name='download_pdf'),
    path('enter-code/', views.enter_quiz_code, name='enter_quiz_code'),
    path('attempt/<int:quiz_id>/', views.attempt_quiz, name='attempt_quiz'),
    path('result/<int:attempt_id>/', views.view_result, name='view_result'),
    path('past-attempts/', views.past_attempts, name='past_attempts'),
    path('join-quiz/', join_quiz, name='join_quiz'),
    path('available/', available_quizzes, name='available_quizzes'),
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
]