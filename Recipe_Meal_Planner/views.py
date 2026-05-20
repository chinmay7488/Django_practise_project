from django.shortcuts import render


def home(request):
    return render(request, "Recipe_Meal_Planner/index.html")
