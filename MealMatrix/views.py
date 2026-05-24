from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import *

def home(request):
    if request.user.is_authenticated:
        return render(request, "Recipe_Meal_Planner/index.html",context={
            "User" : request.user
        })

    return render(request, "Recipe_Meal_Planner/index.html")

def export_Recipe(request):
    return render(request, "Recipe_Meal_Planner/export.html")

def Login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # if remember_me:
            #     request.session.set_expiry(1209600) 
            # else:
            #     request.session.set_expiry(0)
            return redirect('Recipe_Meal_Planner:home')
        else:
            error_messages =  "Invalid username or password."

        return render(request, 'Recipe_Meal_Planner/index.html', {"error_messages": error_messages})

    return render(request, "Recipe_Meal_Planner/login.html")

def logout_page(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('Recipe_Meal_Planner:home')

    auth_logout(request)
    return redirect('Recipe_Meal_Planner:home')

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

def Add_recipe(request):
    Ingredients_name = Ingredients.objects.all()
    recipe_Category  = Recipe_Category.choices
    context={
        "Ingredients": Ingredients_name,
        "Recipe_Category": recipe_Category
    }
    if request.method == "POST":
        Title = request.POST.get("Recipe_title")
        ingredients_list =  request.POST.getlist("ingredient[]")
        ing_quantity_list =  request.POST.getlist("quantity[]")
        ing_unit_list =  request.POST.getlist("unit[]")
        ing_cal_list =  request.POST.getlist("calories[]")
       
        current_owner = request.user.recipe_profile
        Recipes.objects.create(
            Person = current_owner,
            Title = Title,
            Description = request.POST.get("Recipe_time"),
            Prep_time = request.POST.get("Recipe_time"), 
            Category = request.POST.get("Recipe_catergory"),
            Recipe_Photo = request.POST.get("Recipe_photo"),
            Instruction = request.POST.get("Recipe_instr"),
            Recipe_Calories = request.POST.get("Recipe_cal"),
            Recipe_Protein = request.POST.get("Recipe_pro"),
            Recipe_Carbs = request.POST.get("Recipe_carbs"),
            Recipe_Fats = request.POST.get("Recipe_fat"),
        )
        for ing_id, ing_quantity, ing_unit, ing_cal in zip(ingredients_list, ing_quantity_list, ing_unit_list, ing_cal_list):
            Recipe_Bridge_Table.objects.create(
                Recipe_id = Recipes.objects.get(Title = Title),
                Ingredient_id = Ingredients.objects.get(id = ing_id),
                Ingredient_quantity = ing_quantity,
                Ingredient_Unit = ing_unit,
                Ingredient_calories = ing_cal
            )


    return render(request, "Recipe_Meal_Planner/recipe_form.html", context)

def Add_ingredients(request):
    if request.method=="POST":
        Ing_name = request.POST.getlist('name[]')
        calories_gram = request.POST.getlist('calories_gram[]')
        calories_cup = request.POST.getlist('calories_cup[]')
        calories_piece = request.POST.getlist('calories_piece[]')
        print(Ing_name)
        for name, gram, cup, piece in zip(Ing_name, calories_gram, calories_cup, calories_piece):
            Ingredients.objects.create(
                Name = name,
                Calories_gram =gram,
                Calories_cup =cup,
                Calories_piece  =piece

            )
        return redirect("Recipe_Meal_Planner:recipe_add")

    return render(request, "Recipe_Meal_Planner/ingredient_form.html")

def Recipes_page(request):
    return render(request, "Recipe_Meal_Planner/recipes.html")

def Register(request):
    if request.method == "POST":
        username = request.POST.get('Username')
        email = request.POST.get('email')
        number = request.POST.get('phonenumber')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user is not None and RecipeOwner.objects.filter(user=user).exists():
            return render(request, 'Recipe_Meal_Planner/register.html', {"error_messages": "Username already taken!"})

        if user is None:
            user = User.objects.create_user(username=username, email=email, password=password)

        RecipeOwner.objects.create(user=user, Phone_number=number)
        return redirect('Recipe_Meal_Planner:login')

    return render(request, 'Recipe_Meal_Planner/register.html')

def Shopping_list(request):
    return render(request, "Recipe_Meal_Planner/shopping_list.html")

def Smart_Generator(request):
    return render(request, "Recipe_Meal_Planner/smart_generator.html")
