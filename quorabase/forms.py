from django import forms
from django.forms import ModelForm
from .models import Answer


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text"]
