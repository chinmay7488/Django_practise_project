from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

def home(request):
    return render(request, "Recipe_Meal_Planner/index.html")

def export_Recipe(request):
    return render(request, "Recipe_Meal_Planner/export.html")

def Login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember') == "on"

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if remember_me:
                request.session.set_expiry(1209600) 
            else:
                request.session.set_expiry(0)
            return redirect('TAnalyzer:home')
        else:
            error_messages =  "Invalid username or password."

        return render(request, 'Recipe_Meal_Planner/login.html', {"error_messages": error_messages})

    return render(request, "Recipe_Meal_Planner/login.html")

def logout_page(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('TAnalyzer:home')

    return render(request, 'Text_Analyzer/logout.html')

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
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'Recipe_Meal_Planner/register.html', {"error_messages": "Passwords do not match."})

        if User.objects.filter(username=username).exists():
            return render(request, 'Recipe_Meal_Planner/register.html', {"error_messages": "Username already taken!"})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('Recipe_Meal_Planner:login')

    return render(request, 'Recipe_Meal_Planner/register.html')

def Shopping_list(request):
    return render(request, "Recipe_Meal_Planner/shopping_list.html")

def Smart_Generator(request):
    return render(request, "Recipe_Meal_Planner/smart_generator.html")
