from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):

    title = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(auto_now_add=True)
    up_vote = models.ManyToManyField(
        User, related_name="question_up_vote", through="Vote", blank=True
    )
    down_vote = models.ManyToManyField(
        User, related_name="question_down_vote", through="Vote", blank=True
    )


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    time_posted = models.DateTimeField(auto_now_add=True)
    up_vote = models.ManyToManyField(
        User, related_name="answer_up_vote", through="Vote", blank=True
    )
    down_vote = models.ManyToManyField(
        User, related_name="answer_down_vote", through="Vote", blank=True
    )


class Vote(models.Model):
    choice = [("up", "upvote"), ("down", "downvote")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices=choice)
    value = models.IntegerField(choices=[(1, "upvote"), (2, "downvote")])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="", upload_to="path/")
    about = models.TextField(blank=True)
    email = models.EmailField(validators="Regex", default="")
