from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Recipe_Category(models.TextChoices):
    Breakfast = 'Br', 'Breakfast'
    Lunch = 'Lh', 'Lunch'
    Dinner = 'Dr', 'Dinner'


class Recipes(models.Model):
    Person = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.TextField(max_length=100)
    Description = models.TextField()
    Prep_time = models.IntegerField()
    Category = models.TextField(choices=Recipe_Category, default=Recipe_Category.Breakfast)
    Recipe_Photo = models.ImageField()
    Instruction = models.TextField()
    Recipe_Calories = models.IntegerField()
    Recipe_Protein = models.IntegerField()
    Recipe_Carbs = models.IntegerField()
    Recipe_Fats = models.IntegerField()

