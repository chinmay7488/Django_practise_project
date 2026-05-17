from django.contrib import admin
from django.urls import path
from . import views

app_name = 'TAnalyzer'

urlpatterns = [
    path("", views.home, name='home'),
    path("feature/", views.feature, name='feature'),
    path("history/", views.History, name='history'),
    path("profile/", views.Profile, name='profile'),
    path("login/", views.Profile, name='login'),
    path("logout/", views.Profile, name='logout'),
    path("delete/", views.Profile, name='delete'),
]
