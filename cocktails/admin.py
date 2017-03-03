from django.contrib import admin
from .models import Distillery, Manufacturer, Brand
from .models import Ingredient, IngredientClass, IngredientCategory, IngredientSubcategory
from .models import Cocktail, CocktailCategory, Recipe, RecipeIngredient


# Register your models here.
admin.site.register(Distillery)
admin.site.register(Manufacturer)
admin.site.register(Brand)

admin.site.register(Ingredient)
admin.site.register(IngredientSubcategory)
admin.site.register(IngredientCategory)
admin.site.register(IngredientClass)
admin.site.register(Cocktail)
admin.site.register(CocktailCategory)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
