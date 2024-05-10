from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from vote.models import VoteModel


# Create your models here.
class Question(VoteModel,models.Model):  # Table name quorabase_question

    title = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title}"

class Answer(VoteModel,models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-vote_score']
    
    def __str__(self) -> str:
        return f"Answer given by {self.author} to the question {self.question}:{self.text}"