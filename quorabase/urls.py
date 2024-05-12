from django.urls import path
from . import views
from .views import QuestionListView, QuestionDetailView, AskQuestionView,QuestionUpdateView,QuestionDeleteView,AnswerView,AnswerUpdateView

urlpatterns = [
    path("", QuestionListView.as_view(), name="quora-home"),
    path("question/<int:pk>/", QuestionDetailView.as_view(), name="question-detail"),
    path("question/new/", AskQuestionView.as_view(), name="ask-question"),
    path("question/<int:pk>/update/", QuestionUpdateView.as_view(), name="question-update"),
    path("question/<int:pk>/delete/", QuestionDeleteView.as_view(), name="question-delete"),
    path("question/<int:pk>/answer/", AnswerView.as_view(), name="question-answer"),
    path("question/<int:question_pk>/answer/<int:answer_pk>/<str:username>/update/", AnswerUpdateView.as_view(template_name = "quorabase/answer_form.html"), name="answer-update"),
    # path("question/<int:pk>/answer/<str:username>/",AnswerDetailView.as_view(),name="answer-detail"),
]
