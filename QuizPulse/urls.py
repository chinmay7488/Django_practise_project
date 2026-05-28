from django.urls import path

from . import views

app_name = "QuizPulse"

urlpatterns = [
    path("", views.home, name="home"),
    path("start/", views.start_quiz, name="start_quiz"),
    path("question/", views.question, name="question"),
    path("results/", views.results, name="results"),
    path("review/", views.review, name="review"),
    path("restart/", views.restart, name="restart"),
]
