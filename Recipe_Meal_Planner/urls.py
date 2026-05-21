from django.urls import path

from . import views

app_name = "Recipe_Meal_Planner"

urlpatterns = [
    path("", views.home, name="home"),
    path("export/", views.export_Recipe, name="export"),
    path("login/", views.Login_page, name="login"),
    path("meal-planner/", views.Meal_Planner, name="meal_planner"),
    path("nutrition/", views.Nutrition, name="nutrition"),
    path("pantry/", views.Pantry, name="pantry"),
    path("recipes/", views.Recipes, name="recipes"),
    path("recipes/delete/", views.Delete_recipe, name="recipe_delete"),
    path("recipes/detail/", views.Detail_recipe, name="recipe_detail"),
    path("recipes/form/", views.Form_recipe, name="recipe_form"),
    path("register/", views.Register, name="register"),
    path("shopping-list/", views.Shopping_list, name="shopping_list"),
    path("smart-generator/", views.Smart_Generator, name="smart_generator"),
]
