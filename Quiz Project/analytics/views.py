import os
import matplotlib.pyplot as plt
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from quiz.models import Quiz, Attempt


@login_required
def analytics_dashboard(request):

    quizzes = Quiz.objects.filter(created_by=request.user)
    attempts = Attempt.objects.filter(quiz__in=quizzes)

    total_quizzes = quizzes.count()
    total_attempts = attempts.count()
    avg_score = attempts.aggregate(Avg('percentage'))['percentage__avg']
    avg_score = round(avg_score, 2) if avg_score else 0

    # Create media folder
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    # -------- Bar Chart --------
    labels = []
    data = []

    for quiz in quizzes:
        avg = Attempt.objects.filter(quiz=quiz).aggregate(
            Avg('percentage')
        )['percentage__avg']

        labels.append(quiz.title)
        data.append(round(avg, 2) if avg else 0)

    bar_path = os.path.join(settings.MEDIA_ROOT, "analytics_bar.png")

    if quizzes.exists():
        plt.figure(figsize=(6,4))
        plt.bar(labels if labels else ["No Data"],
                data if data else [0])
        plt.title("Quiz Performance")
        plt.ylabel("Average Score (%)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig(bar_path)
        plt.close()

    # -------- Pie Chart --------
    pass_count = attempts.filter(percentage__gte=40).count()
    fail_count = attempts.filter(percentage__lt=40).count()

    pie_path = os.path.join(settings.MEDIA_ROOT, "analytics_pie.png")

    if total_attempts > 0:
        plt.figure(figsize=(5,5))
        plt.pie([pass_count, fail_count],
                labels=["Pass", "Fail"],
                autopct="%1.1f%%")
        plt.title("Pass vs Fail Ratio")
        plt.savefig(pie_path)
        plt.close()

    context = {
        "total_quizzes": total_quizzes,
        "total_attempts": total_attempts,
        "avg_score": avg_score,
    }

    return render(request, "analytics/dashboard.html", context)