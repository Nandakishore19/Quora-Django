from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from vote.models import VoteModel
from django.urls import reverse


# Create your models here.
class Question(models.Model):  # Table name quorabase_question

    title = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vote = models.ManyToManyField(User, related_name="question_vote", blank=True)

    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(
        self,
    ):  # Setting the instance of a specific question to the question detail url.
        return reverse("question-detail", kwargs={"pk": self.pk})


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vote = models.ManyToManyField(User, related_name="answer_vote", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return (
            f"Answer given by {self.author} to the question {self.question}:{self.text}"
        )

    def get_absolute_url(
        self,
    ):  # Setting the instance of a specific question to the question detail url.
        return reverse("question-detail", kwargs={"pk": self.question_id})
