from django.db.models import Avg
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from quiz.models import Option, Quiz, Question, Attempt

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role=role
        )

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

import os
import matplotlib.pyplot as plt
from django.conf import settings
from quiz.models import Quiz, Question, Attempt

@login_required
def teacher_dashboard(request):

    quizzes = Quiz.objects.filter(created_by=request.user)

    total_quizzes = quizzes.count()
    total_questions = Question.objects.filter(quiz__in=quizzes).count()
    total_attempts = Attempt.objects.filter(quiz__in=quizzes).count()

    # --------- ANALYTICS CHART GENERATION ----------
    labels = []
    data = []

    for quiz in quizzes:
        attempts = Attempt.objects.filter(quiz=quiz)

        if attempts.exists():
            avg = sum(a.percentage for a in attempts) / attempts.count()
            labels.append(quiz.title)
            data.append(avg)

    # Create media folder if not exists
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    chart_path = os.path.join(settings.MEDIA_ROOT, "quiz_chart.png")

    # Always generate chart if quizzes exist
    if quizzes.exists():
        plt.figure(figsize=(6,4))

        if data:
            plt.bar(labels, data)
        else:
            plt.bar(["No Data"], [0])

        plt.xlabel("Quizzes")
        plt.ylabel("Average Score (%)")
        plt.title("Quiz Performance")

        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()

    context = {
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
        'total_attempts': total_attempts,
        'quizzes': quizzes,
    }

    return render(request, 'accounts/teacher_dashboard.html', context)
@login_required
def view_results(request):

    if request.user.role != 'teacher':
        return redirect('student_dashboard')

    quizzes = Quiz.objects.filter(created_by=request.user)

    attempts = Attempt.objects.filter(
        quiz__in=quizzes
    ).order_by('-submitted_at')

    return render(request, 'accounts/view_results.html', {
        'attempts': attempts
    })

@login_required
def student_dashboard(request):

    if request.user.role != 'student':
        return redirect('teacher_dashboard')

    attempts = Attempt.objects.filter(student=request.user)

    total_attempts = attempts.count()

    average_score = 0
    highest_score = 0

    if total_attempts > 0:
        average_score = round(
            sum(a.percentage for a in attempts) / total_attempts, 2
        )
        highest_score = max(a.percentage for a in attempts)
    show_result_id = request.GET.get('show_result')
    last_attempt = None
    if show_result_id:
        last_attempt = Attempt.objects.filter(id=show_result_id, student=request.user).first()

    context = {
        'total_attempts': total_attempts,
        'average_score': average_score,
        'highest_score': highest_score, 'last_attempt': last_attempt,
    }

    return render(request, 'accounts/student_dashboard.html', context)

@login_required
def analytics_page(request):

    quizzes = Quiz.objects.filter(created_by=request.user)
    attempts = Attempt.objects.filter(quiz__in=quizzes)

    total_quizzes = quizzes.count()
    total_attempts = attempts.count()

    average_score = attempts.aggregate(Avg('percentage'))['percentage__avg']
    average_score = round(average_score, 2) if average_score else 0

    # -------- Create Media Folder --------
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    # -------- BAR CHART --------
    labels = []
    data = []

    for quiz in quizzes:
        avg = Attempt.objects.filter(quiz=quiz).aggregate(
            Avg('percentage')
        )['percentage__avg']

        labels.append(quiz.title)
        data.append(round(avg, 2) if avg else 0)

    bar_chart_path = os.path.join(settings.MEDIA_ROOT, "bar_chart.png")

    if quizzes.exists():
        plt.figure(figsize=(6,4))
        plt.bar(labels if labels else ["No Data"],
                data if data else [0])
        plt.xlabel("Quizzes")
        plt.ylabel("Average Score (%)")
        plt.title("Quiz Performance")
        plt.tight_layout()
        plt.savefig(bar_chart_path)
        plt.close()

    # -------- PIE CHART --------
    pass_count = attempts.filter(percentage__gte=40).count()
    fail_count = attempts.filter(percentage__lt=40).count()

    pie_chart_path = os.path.join(settings.MEDIA_ROOT, "pie_chart.png")

    if total_attempts > 0:
        plt.figure(figsize=(5,5))
        plt.pie([pass_count, fail_count],
                labels=["Pass", "Fail"],
                autopct="%1.1f%%")
        plt.title("Pass vs Fail Distribution")
        plt.savefig(pie_chart_path)
        plt.close()

    context = {
        "total_quizzes": total_quizzes,
        "total_attempts": total_attempts,
        "average_score": average_score,
    }

    return render(request, "accounts/analytics.html", context)
