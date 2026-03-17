from django import forms
from .models import Quiz, Question,Option
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ['created_by', 'quiz_code']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'timer': forms.NumberInput(attrs={'class': 'form-control'}),
            'negative_marking': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_attempts': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'marks']
        widgets = {
            'quiz': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['question', 'text', 'is_correct']