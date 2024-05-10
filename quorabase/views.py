from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView,DetailView


# Create your views here.
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
