from django.shortcuts import render
from django.http import HttpResponse,Http404
from .models import Question, Answer
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
class AnswerUpdateView(LoginRequiredMixin,UpdateView):
    model = Answer
    fields = ["text"]
    

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question_id = self.kwargs["question_pk"]
        # import pdb; pdb.set_trace()
        return super().form_valid(form)

    def test_func(self):
        answer_id = self.kwargs.get('answer_pk')
        print(answer_id)
        import pdb; pdb.set_trace()
        return self.request.user.answer_set.filter(pk=answer_id).exists()
     
    def get_object(self, queryset=None):
        answer_id = self.kwargs.get('answer_pk')
        answer = Answer.objects.get(pk = answer_id)
        return answer
    

class AnswerDeleteView(LoginRequiredMixin,DeleteView):
    model = Answer
    queryset = Answer.objects.all()

    def get_success_url(self) -> str:
        question = self.kwargs.get('pk')
        return reverse("{%url 'question-detail' question%}")