from django.db import models
from django.conf import settings


class MealPlanEntry(models.Model):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"

    MEAL_TYPE_CHOICES = [
        (BREAKFAST, "Breakfast"),
        (LUNCH, "Lunch"),
        (DINNER, "Dinner"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="meal_plan_entries",
    )
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    mealdb_id = models.CharField(max_length=20)
    meal_name = models.CharField(max_length=255)
    meal_thumb = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date", "meal_type"],
                name="unique_meal_plan_slot",
            )
        ]
        ordering = ["date", "meal_type"]

    def __str__(self):
        return f"{self.user} | {self.date} | {self.meal_type} | {self.mealdb_id}"
