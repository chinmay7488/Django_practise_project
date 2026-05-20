from django.urls import path

from . import views

app_name = "Recipe_Meal_Planner"

urlpatterns = [
    path("", views.home, name="home"),
]
