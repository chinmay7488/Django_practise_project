from django.contrib import admin
from django.urls import path
from . import views

app_name = 'TAnalyzer'

urlpatterns = [
    path("", views.home, name='home'),
    path("feature/", views.feature, name='feature'),
    path("history/", views.History, name='history'),
    path("profile/", views.Profile, name='profile'),
    path("login/", views.login_page, name='login'),
    path("signup/", views.signup, name='signup'),
    path("logout/", views.logout_page, name='logout'),
    path("delete/", views.delete, name='delete'),
    path("save/", views.Save_Analyze, name='save_analyze'),
    path("delete_analyze/<int:analyzeid>/", views.delete_analyze, name='delete_analyze'),

]
