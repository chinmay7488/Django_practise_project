from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Recipes)
admin.site.register(Ingredients)
admin.site.register(RecipeOwner)