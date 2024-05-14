from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from .models import Question, Answer
from django.db.models import Count
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from vote.models import VoteModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
# AskquestionView
# QeustionDetail
# AnswerView
# AnswerDetailView
# AnswerUpdateView
# AnswerDeleteView
# QNAListView
# Vote


def home(request):
    context = {"posts": Question.objects.all()}
    return render(request, "quorabase/home.html", context=context)


class QuestionListView(ListView):
    model = Question
    template_name = "quorabase/home.html"  # By default Django would look for a template named <app>/<model>_<viewtype>.html
    context_object_name = "questions"
    ordering = ["-created_at"]


class QuestionDetailView(DetailView):
    model = Question
    queryset = Question.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()  # Retrieve the current question object

        # Annotate the queryset of answers with the count of votes
        answers = question.answer_set.annotate(num_votes=Count("vote"))

        # Order answers by the number of votes (descending) and then by created_at (descending)
        answers = answers.order_by("-num_votes", "-created_at")

        context["answers"] = answers  # Add ordered answers to the context
        return context


class AskQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ["title"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = ["title"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(
        self,
    ):  # UserPassesTestMixin Uses this test_func to test if the author of the question is the only one trying to update it
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    queryset = Question.objects.all()
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class AnswerView(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ["text"]

    # success_url = ""
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question_id = self.kwargs["pk"]
        return super().form_valid(form)

    # def get_context_data(self,**kwargs):
    #     context = super(AnswerView,self).get_context_data(**kwargs)
    #     question = Question.objects.get(self.kwargs['pk'])
    #     context['question'] = question
    # return context


# class AnswerDetailView(DetailView):
#     model = Answer
#     queryset = Answer.objects.all()
class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    fields = ["text"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question_id = self.kwargs["question_pk"]
        # import pdb; pdb.set_trace()
        return super().form_valid(form)

    def test_func(self):
        answer_id = self.kwargs.get("answer_pk")
        print(answer_id)
        # import pdb; pdb.set_trace()
        return self.request.user.answer_set.filter(pk=answer_id).exists()

    def get_object(self, queryset=None):
        answer_id = self.kwargs.get("answer_pk")
        answer = Answer.objects.get(pk=answer_id)
        return answer


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    queryset = Answer.objects.all()

    def get_success_url(self) -> str:
        question = self.kwargs.get("question_pk")
        return reverse("question-detail", kwargs={"pk": question})

    def get_object(self, queryset=None):
        answer_id = self.kwargs.get("answer_pk")
        answer = Answer.objects.get(pk=answer_id)
        return answer

    def test_func(self):
        answer = self.get_object()

        return self.request.user == answer.author


@login_required
def upvote_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    if user in question.vote.all():
        question.vote.remove(user)
    else:
        question.vote.add(user)
    return redirect("quora-home")


@login_required
def upvote_answer(request, question_id, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    user = request.user
    if user in answer.vote.all():
        answer.vote.remove(user)
    else:
        answer.vote.add(user)
    return redirect("question-detail", pk=answer.question_id)


class AboutUser(ListView):
    model = Question
    template_name = "quorabase/about.html"
    context_object_name = "questions"
    ordering = ["-vote"]

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Question.objects.filter(author=user).order_by("-vote")


class UserPostQuestions(ListView):
    model = Question
    context_object_name = "questions"
    template_name = "quorabase/questions.html"
    ordering = ["-vote"]

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Question.objects.filter(author=user).order_by("-vote")


class UserPostAnswers(ListView):
    model = Answer
    context_object_name = "answers"
    template_name = "quorabase/answers.html"
    ordering = ["-vote"]

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Answer.objects.filter(author=user).order_by("-vote")
