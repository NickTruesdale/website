from django.contrib import admin
from .models import Ingredient, IngredientClass, IngredientCategory, IngredientSubcategory, Distillery, Manufacturer


# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Distillery)
admin.site.register(Manufacturer)
admin.site.register(IngredientSubcategory)
admin.site.register(IngredientCategory)
admin.site.register(IngredientClass)
