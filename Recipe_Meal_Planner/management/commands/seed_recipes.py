import pandas as pd
import os
import regex as re
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from Recipe_Meal_Planner.models import Recipes, RecipeOwner, Ingredients, Recipe_Bridge_Table, Ingredient_unit


class Command(BaseCommand):
    help = 'Seeds fake recipe data from a CSV file into the database'
    def get_recipe_image_path(profile, filename):
        """
        Generates a dynamic upload path: media/recipe_images/<username>/<filename>
        instance: The actual Recipes model object being saved
        filename: The original name of the uploaded image file (e.g., 'pancake.jpg')
        """
        # 1. Grab the username from the linked RecipeOwner -> User profile
        user = RecipeOwner.objects.get(user__username='sahil')
        
        # 2. Extract the file extension (e.g., '.jpg', '.png')
        ext = filename.split('.')[-1]
        
        # 3. Clean or format the file name if you want (Optional: use recipe title as name)
        # clean_title = instance.Title.replace(" ", "_").lower()
        # filename = f"{clean_title}.{ext}"
        
        # 4. Return the path relative to your MEDIA_ROOT folder
        return os.path.join('recipe_images', user.user.username, filename)
    
    def handle(self, *args, **options):

        df = pd.read_csv(r'D:\Subject\Code Practise\Django_Practise\DjangoPractisePro\Recipe_Meal_Planner\Sample Data\recipes_master_list.csv')
        print(df.columns)
        profile = RecipeOwner.objects.get(user__username='sahil')

        for index, row in df.iterrows():
            lines = row['list of ingredients used (ingredient_name, quantity, unit, calories)'].strip().split('\n')
            recipe_ingredients = []
            missing_ingredients = []
            unit_choices = {
                'grams': Ingredient_unit.Gram,
                'cups': Ingredient_unit.Cup,
                'piece': Ingredient_unit.Piece,
            }

            for line_num, line in enumerate(lines, 1):
                items = line.split('|')
                for item in items:
                    clean_item = item.strip().strip('()')
                    details = [d.strip() for d in clean_item.split(';')]
                    if len(details) != 4:
                        continue

                    name, quantity, unit, calories = details
                    ingredient = Ingredients.objects.filter(Name=name).first()
                    if ingredient is None:
                        missing_ingredients.append(name)
                        continue

                    u = unit_choices.get(unit)
                    if u is None:
                        continue

                    recipe_ingredients.append({
                        'ingredient': ingredient,
                        'quantity': quantity,
                        'unit': u,
                        'calories': calories,
                    })

            if missing_ingredients:
                missing_names = ', '.join(sorted(set(missing_ingredients)))
                print(f"Skipping recipe '{row['recipe_title']}' because ingredients are missing: {missing_names}")
                continue

            recipe = Recipes.objects.create(
               Person = profile,
                Title = row['recipe_title'],
                Description = row['description'],
                Prep_time = row['preparation_time'].split()[0], 
                Category = row['category'],
                Recipe_Photo = Command.get_recipe_image_path(profile, r"C:\Users\chinm\Downloads\download.jpg"),
                Instruction = row['instruction'],
                Recipe_Calories =row['calories'],
                Recipe_Protein =int(re.search(r'\d+', row['protein']).group()),
                Recipe_Carbs =int(re.search(r'\d+', row['carbs']).group()),
                Recipe_Fats = int(re.search(r'\d+', row['fats']).group()),
            )

            for ingredient_data in recipe_ingredients:
                Recipe_Bridge_Table.objects.create(
                    Recipe_id = recipe,
                    Ingredient_id = ingredient_data['ingredient'],
                    Ingredient_quantity = ingredient_data['quantity'],
                    Ingredient_Unit = ingredient_data['unit'],
                    Ingredient_calories = ingredient_data['calories'].split()[0]
                )
