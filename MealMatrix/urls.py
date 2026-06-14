from django.urls import path

from . import views

app_name = "MealMatrix"

urlpatterns = [
    path("", views.home, name="home"),
    path("export/", views.export_Recipe, name="export"),
    path("login/", views.Login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("meal-planner/", views.Meal_Planner, name="meal_planner"),
    path("meal-planner/add/", views.Add_meal_to_plan, name="meal_plan_add"),
    path("nutrition/", views.Nutrition, name="nutrition"),
    path("pantry/", views.Pantry, name="pantry"),
    path("categories/", views.Categories_page, name="categories"),
    path("recipes/", views.Recipes_page, name="recipes"),
    path("recipes/delete/", views.Delete_recipe, name="recipe_delete"),
    path("recipes/add/", views.Add_recipe, name="recipe_add"),
    path("recipes/detail/", views.Detail_recipe, name="recipe_detail"),
    path("recipes/form/", views.Add_ingredients, name="recipe_form"),
    path("ingredients/add/", views.Add_ingredients, name="ingredient_add"),
    path("register/", views.Register, name="register"),
    path("shopping-list/", views.Shopping_list, name="shopping_list"),
    path("smart-generator/", views.Smart_Generator, name="smart_generator"),
]
