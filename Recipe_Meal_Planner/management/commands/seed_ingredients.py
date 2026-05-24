import pandas as pd
from django.core.management.base import BaseCommand
from Recipe_Meal_Planner.models import Ingredients


class Command(BaseCommand):
    help = 'Seeds fake recipe data from a CSV file into the database'

    def handle(self, *args, **options):

        df = pd.read_csv(r'D:\Subject\Code Practise\Django_Practise\DjangoPractisePro\Recipe_Meal_Planner\Sample Data\ingredients_master_list.csv')
        created_count = 0
        updated_count = 0

        for index, row in df.iterrows():
            ingredient, created = Ingredients.objects.update_or_create(
                Name=row['ingredient_name'],
                defaults={
                    'Calories_gram': row['calories per gram'],
                    'Calories_cup': row['calories per cup'],
                    'Calories_piece': str(row['calories per piece']).split()[0],
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        print(f"Ingredients seed completed. Created: {created_count}, Updated: {updated_count}")

