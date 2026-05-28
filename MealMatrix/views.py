from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import *
import requests
import random

MealDB_BASE_url = "https://www.themealdb.com/api/json/v1/1/"
CalorieNinjas_API_KEY = 'hgjhLLbxtolxEeL2Ge1DUCTsIHYFrDQDS4qo2m92'
CalorieNinjas_url = "https://api.calorieninjas.com/v1/nutrition?query="
category_filter_addon = 'filter.php?c='
ingredient_filter_addon = 'filter.php?i='
ingredient_api_addon = 'list.php?i=list'
Category_List =[]
Ingredient_List =[]

def home(request):
    if len(Category_List) == 0:
        category_url = f"{MealDB_BASE_url}{"categories.php"}"   
        respone_cat = requests.get(category_url).json()['categories']
        for cat in respone_cat:
            Category_List.append(cat)

    if len(Ingredient_List) == 0:
        ingredient_url = f"{MealDB_BASE_url}{ingredient_api_addon}"
        respone_ing = requests.get(ingredient_url).json()['meals']
        for ing in respone_ing:
            Ingredient_List.append(ing)

    if request.user.is_authenticated:
        return render(request, "MealMatrix/index.html",context={
            "User" : request.user
        })

    return render(request, "MealMatrix/index.html")

def export_Recipe(request):
    return render(request, "MealMatrix/export.html")

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
            return redirect('MealMatrix:home')
        else:
            error_messages =  "Invalid username or password."

        return render(request, 'MealMatrix/index.html', {"error_messages": error_messages})

    return render(request, "MealMatrix/login.html")

def logout_page(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('MealMatrix:home')

    auth_logout(request)
    return redirect('MealMatrix:home')

def Meal_Planner(request):
    return render(request, "MealMatrix/meal_planner.html")

def Nutrition(request):
    return render(request, "MealMatrix/nutrition.html")

def Pantry(request):
    return render(request, "MealMatrix/pantry.html")

def Delete_recipe(request):
    return render(request, "MealMatrix/recipe_delete.html")

def Detail_recipe(request):
    return render(request, "MealMatrix/recipe_detail.html")

def Add_recipe(request):
    # Ingredients_name = Ingredients.objects.all()
    # recipe_Category  = Recipe_Category.choices
    # context={
    #     "Ingredients": Ingredients_name,
    #     "Recipe_Category": recipe_Category
    # }
    # if request.method == "POST":
    #     Title = request.POST.get("Recipe_title")
    #     ingredients_list =  request.POST.getlist("ingredient[]")
    #     ing_quantity_list =  request.POST.getlist("quantity[]")
    #     ing_unit_list =  request.POST.getlist("unit[]")
    #     ing_cal_list =  request.POST.getlist("calories[]")
       
    #     current_owner = request.user.recipe_profile
    #     Recipes.objects.create(
    #         Person = current_owner,
    #         Title = Title,
    #         Description = request.POST.get("Recipe_time"),
    #         Prep_time = request.POST.get("Recipe_time"), 
    #         Category = request.POST.get("Recipe_catergory"),
    #         Recipe_Photo = request.POST.get("Recipe_photo"),
    #         Instruction = request.POST.get("Recipe_instr"),
    #         Recipe_Calories = request.POST.get("Recipe_cal"),
    #         Recipe_Protein = request.POST.get("Recipe_pro"),
    #         Recipe_Carbs = request.POST.get("Recipe_carbs"),
    #         Recipe_Fats = request.POST.get("Recipe_fat"),
    #     )
    #     for ing_id, ing_quantity, ing_unit, ing_cal in zip(ingredients_list, ing_quantity_list, ing_unit_list, ing_cal_list):
    #         Recipe_Bridge_Table.objects.create(
    #             Recipe_id = Recipes.objects.get(Title = Title),
    #             Ingredient_id = Ingredients.objects.get(id = ing_id),
    #             Ingredient_quantity = ing_quantity,
    #             Ingredient_Unit = ing_unit,
    #             Ingredient_calories = ing_cal
    #         )


    return render(request, "MealMatrix/recipe_form.html")

def Add_ingredients(request):
    # if request.method=="POST":
    #     Ing_name = request.POST.getlist('name[]')
    #     calories_gram = request.POST.getlist('calories_gram[]')
    #     calories_cup = request.POST.getlist('calories_cup[]')
    #     calories_piece = request.POST.getlist('calories_piece[]')
    #     print(Ing_name)
    #     for name, gram, cup, piece in zip(Ing_name, calories_gram, calories_cup, calories_piece):
    #         Ingredients.objects.create(
    #             Name = name,
    #             Calories_gram =gram,
    #             Calories_cup =cup,
    #             Calories_piece  =piece

    #         )
    #     return redirect("MealMatrix:recipe_add")

    return render(request, "MealMatrix/ingredient_form.html")

def Recipes_page(request):
    datacontext = {
        "CategoryList" : Category_List,
        "IngredientList" : Ingredient_List,
    }
    category_filter = request.GET.get('category')
    ingredient_filter = request.GET.get('ingredient')
    
    url ="" 
    cat = ""
    ing=""
    filt_recipes=[]
    if category_filter:
        for i in Category_List:
            if i['idCategory'] == category_filter:
                url = f"{MealDB_BASE_url}{category_filter_addon}{i['strCategory']}"
                cat = i['strCategory']
                filt_recipes = filt_recipes + (requests.get(url).json()['meals'])
                break
            
    if ingredient_filter:
        for i in Ingredient_List:
            if i['idIngredient'] == ingredient_filter:
                url = f"{MealDB_BASE_url}{ingredient_filter_addon}{i['idIngredient']}"
                ing = i['idIngredient']
                filt_recipes.append(requests.get(url).json()['meals'])
                break

    # print(filt_recipes)
    if  filt_recipes: 
        datacontext.update({'Recipes': filt_recipes, 'Category': cat, 'Ingredient': ing})
        return render(request, 'MealMatrix/recipes.html', context= datacontext)

    else:
        recipes=[]
        for cat in Category_List:
            url = f"{MealDB_BASE_url}{category_filter_addon}{cat['strCategory']}"
            recipes.extend(requests.get(url).json()['meals'])

        random.shuffle(recipes)
        datacontext.update({'Recipes': recipes, 'Category': cat, 'Ingredient': ing})
        return render(request, 'MealMatrix/recipes.html', context= datacontext)

    # if ingredient_filter:
    #     for i in Ingredient_List:
    #         if i['idIngredient'] == str(id):
    #             print('Found in ingredientcls')
    #             break        


    # Option B: Get all recipes in a major category (Uncomment if you prefer this)
    # api_url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=Seafood"
    
    # try:
    #     response = requests.get(api_url)
    #     data = response.json()
    #     all_meals = data.get('meals') or []
        
    #     # Mix them up randomly so the homepage looks different on refresh
    #     random.shuffle(all_meals)
        
    #     # Python slice syntax: Grab exactly the first 20 or 50 items
    #     recipes_to_show = all_meals[:20] 
        
    # except Exception as e:
    #     print(f"API Fetch Error: {e}")
    #     recipes_to_show = []

    return render(request, 'MealMatrix/recipes.html')

def Categories_page(request):
   

    return render(request, "MealMatrix/categories.html", context={"Categories": Category_List})

def Register(request):
    # if request.method == "POST":
    #     username = request.POST.get('Username')
    #     email = request.POST.get('email')
    #     number = request.POST.get('phonenumber')
    #     password = request.POST.get('password')

    #     user = User.objects.filter(username=username).first()

    #     if user is not None and RecipeOwner.objects.filter(user=user).exists():
    #         return render(request, 'MealMatrix/register.html', {"error_messages": "Username already taken!"})

    #     if user is None:
    #         user = User.objects.create_user(username=username, email=email, password=password)

    #     RecipeOwner.objects.create(user=user, Phone_number=number)
    #     return redirect('MealMatrix:login')

    return render(request, 'MealMatrix/register.html')

def Shopping_list(request):
    return render(request, "MealMatrix/shopping_list.html")

def Smart_Generator(request):
    return render(request, "MealMatrix/smart_generator.html")
