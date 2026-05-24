from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class Recipe_Category(models.TextChoices):
    Breakfast = 'Br', 'Breakfast'
    Lunch = 'Lh', 'Lunch'
    Dinner = 'Dr', 'Dinner'
    Snack = 'Sn', 'Snack' 
    Dessert= 'Ds', 'Dessert'

class Ingredient_unit(models.TextChoices):
    Gram = 'g', 'Gram'
    Cup = 'c', 'Cup'
    Piece = 'p', 'Piece'

class RecipeOwner(models.Model):
    # Link directly to the main user model. 
    # If the main user is deleted, this app-specific profile is deleted too.
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='recipe_profile'
    )
    Phone_number = models.IntegerField(max_length=10)

class Ingredients(models.Model):
    Name = models.TextField(max_length=50)
    Calories_gram = models.IntegerField()
    Calories_cup = models.IntegerField()
    Calories_piece = models.IntegerField()

class Recipes(models.Model):
    Person = models.ForeignKey(RecipeOwner, on_delete=models.CASCADE)
    Title = models.TextField(max_length=100)
    Description = models.TextField()
    Prep_time = models.IntegerField()
    Category = models.TextField(choices=Recipe_Category, default=Recipe_Category.Breakfast)
    Recipe_Photo = models.ImageField(upload_to='Recipes/Photo')
    Instruction = models.TextField()
    Recipe_Calories = models.IntegerField()
    Recipe_Protein = models.IntegerField()
    Recipe_Carbs = models.IntegerField()
    Recipe_Fats = models.IntegerField()
    Ingredients = models.ManyToManyField(Ingredients, through='Recipe_Bridge_Table')


    
class Recipe_Bridge_Table(models.Model):
    Recipe_id = models.ForeignKey(Recipes,on_delete=models.CASCADE, related_name="Recipe_id")
    Ingredient_id = models.ForeignKey(Ingredients,on_delete=models.CASCADE, related_name="Ingredient_id")
    Ingredient_quantity = models.IntegerField()
    Ingredient_Unit = models.CharField(max_length=2, choices=Ingredient_unit, default=Ingredient_unit.Gram)
    Ingredient_calories = models.IntegerField()

