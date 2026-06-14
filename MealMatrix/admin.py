from django.contrib import admin
from .models import MealPlanEntry


@admin.register(MealPlanEntry)
class MealPlanEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "meal_type", "meal_name", "mealdb_id")
    list_filter = ("meal_type", "date")
    search_fields = ("user__username", "meal_name", "mealdb_id")
