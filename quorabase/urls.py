from django.urls import path
from . import views
from .views import QuestionListView,QuestionDetailView

urlpatterns = [
    path("", QuestionListView.as_view(), name="quora-home"),
    path("question/<int:pk>",QuestionDetailView.as_view(),name='question-detail'),
]
