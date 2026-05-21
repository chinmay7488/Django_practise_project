from django.shortcuts import render


def home(request):
    return render(request, "Recipe_Meal_Planner/index.html")

def export_Recipe(request):
    return render(request, "Recipe_Meal_Planner/export.html")

def Login_page(request):
    return render(request, "Recipe_Meal_Planner/login.html")

def Meal_Planner(request):
    return render(request, "Recipe_Meal_Planner/meal_planner.html")

def Nutrition(request):
    return render(request, "Recipe_Meal_Planner/nutrition.html")

def Pantry(request):
    return render(request, "Recipe_Meal_Planner/pantry.html")

def Delete_recipe(request):
    return render(request, "Recipe_Meal_Planner/recipe_delete.html")

def Detail_recipe(request):
    return render(request, "Recipe_Meal_Planner/recipe_detail.html")

def Form_recipe(request):
    return render(request, "Recipe_Meal_Planner/recipe_form.html")

def Recipes(request):
    return render(request, "Recipe_Meal_Planner/recipes.html")

def Register(request):
    return render(request, "Recipe_Meal_Planner/register.html")

def Shopping_list(request):
    return render(request, "Recipe_Meal_Planner/shopping_list.html")

def Smart_Generator(request):
    return render(request, "Recipe_Meal_Planner/smart_generator.html")
