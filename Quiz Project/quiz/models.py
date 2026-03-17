from django.db import models
from django.conf import settings
import random
import string

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    timer = models.IntegerField(default=10)
    negative_marking = models.FloatField(default=0)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    quiz_code = models.CharField(max_length=8, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.quiz_code:
            self.quiz_code = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=6)
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    marks = models.IntegerField(default=1)

    def __str__(self):
        return self.text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
class Attempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.FloatField()
    total_marks = models.FloatField()
    percentage = models.FloatField()
    rank = models.IntegerField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)