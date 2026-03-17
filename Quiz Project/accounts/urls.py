from django.urls import path
from . import views
from quiz import views as quiz_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('results/', views.view_results, name='view_results'),
    path('create-quiz/', quiz_views.create_quiz, name='create_quiz'),
    path('add-question/<int:quiz_id>/', quiz_views.add_question, name='add_question'),
    path('analytics/', views.analytics_page, name='analytics_page'),
]