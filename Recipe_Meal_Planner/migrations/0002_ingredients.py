# Generated manually because project settings currently block makemigrations.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Recipe_Meal_Planner", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ingredients",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.TextField(max_length=50)),
                ("Calories_gram", models.IntegerField()),
                ("Calories_cup", models.IntegerField()),
                ("Calories_piece", models.IntegerField()),
                (
                    "Recipe",
                    models.ManyToManyField(
                        related_name="Recipe",
                        to="Recipe_Meal_Planner.recipes",
                    ),
                ),
            ],
        ),
    ]
