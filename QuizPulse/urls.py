from django.urls import path

from . import views

app_name = "QuizPulse"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_page, name="logout"),
    path("start/", views.start_quiz, name="start_quiz"),
    path("question/", views.question, name="question"),
    path("results/", views.results, name="results"),
    path("review/", views.review, name="review"),
    path("review/<int:attempt_id>/", views.review, name="review_attempt"),
    path("review/<int:attempt_id>/delete/", views.delete_attempt, name="delete_attempt"),
    path("restart/", views.restart, name="restart"),
]
