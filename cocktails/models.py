'''
Module: cocktails.models.py

Description: This module contains models necessary to describe
cocktail recipes. This is a hierarchy of objects:

Drink --> Recipe(s) --> Ingredient(s)
'''

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django_countries.fields import CountryField
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField

from djfractions.models import DecimalFractionField
from decimal import Decimal


# ---------
# Constants
# ---------
NAME_LENGTH_SHORT = 20
NAME_LENGTH_MED = 40
NAME_LENGTH_LONG = 60
URL_LENGTH = 300


#
#
#
class BaseObjectWithImage(models.Model):
    ''' Base class that most of the tables share '''
    name = models.CharField(max_length=NAME_LENGTH_LONG)
    description = models.TextField(default='', blank=True)

    image_url = models.URLField(max_length=URL_LENGTH, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# ----------------
# AUXILIARY TABLES
# ----------------
class UnitOfMeasure(models.Model):
    ''' Units used to measure ingredients in a recipe or glass '''
    name = models.CharField(max_length=NAME_LENGTH_SHORT)
    plural = models.CharField(max_length=NAME_LENGTH_SHORT)

    class Meta:
        verbose_name_plural = 'units of measure'


class Glassware(BaseObjectWithImage):
    ''' Type of glassware and other cups '''

    # Volume
    volume = models.DecimalField(decimal_places=2, max_digits=5)
    unit = models.ForeignKey(UnitOfMeasure, related_name='glassware', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'glassware'

class Tool(BaseObjectWithImage):
    ''' Cocktail hardware (i.e. shakers, spoons, jiggers, etc.) '''
    # What else do we need here besides the description?
    # Brand? Material? Volume?


class PreparationMethod(models.Model):
    ''' Methods that are used to make cocktails '''
    name = models.CharField(max_length=NAME_LENGTH_SHORT)
    description = models.TextField()


class Manufacturer(models.Model):
    ''' Manufaturer of spirits, hardware and other products '''
    name = models.CharField(max_length=NAME_LENGTH_MED)
    description = models.TextField(default='', blank=True)

    # Location
    country = CountryField()
    us_state = USStateField(choices=STATE_CHOICES, verbose_name='state', null=True, blank=True)
    city = models.CharField(max_length=NAME_LENGTH_LONG, null=True, blank=True)

    # Website links
    own_url = models.URLField(
        max_length=URL_LENGTH,
        verbose_name = 'Manufacturer URL',
        null=True,
        blank=True
    )
    wiki_url = models.URLField(
        max_length=URL_LENGTH,
        verbose_name = 'Wikipedia URL',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Distillery(models.Model):
    ''' Location where a spirit is distilled. This is often different than
        the manufacturer since many brands have been bought or have parent
        companies.
    '''
    name = models.CharField(max_length=NAME_LENGTH_MED)
    description = models.TextField(default='', blank=True)

    # Location
    country = CountryField()
    us_state = USStateField(choices=STATE_CHOICES, null=True, blank=True)
    city = models.CharField(max_length=NAME_LENGTH_LONG, null=True, blank=True)

    # Website links
    wiki_url = models.URLField(
        max_length=URL_LENGTH,
        verbose_name = 'Wikipedia URL',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural: 'distilleries'

    def __str__(self):
        return self.name


class CocktailCategory(models.Model):
    ''' Types of cocktails (Flip, fizz, julep, punch, etc.) '''
    name = models.CharField(max_length=40)
    description = models.TextField()

    # How is this drink traditionally composed?
    method = models.ForeignKey(PreparationMethod, related_name='categories', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'cocktail categories'


class IngredientClass(models.Model):
    ''' Umbrella for major ingredient types. Mostly used for sorting
        and differentiating spirits, liqueurs and non-alcoholic ingredients.
    '''
    name = models.CharField(max_length=NAME_LENGTH_SHORT)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'ingredient classes'

    def __str__(self):
        return self.name


class IngredientCategory(BaseObjectWithImage):
    ''' Major category for ingredients '''
    name = models.CharField(max_length=NAME_LENGTH_SHORT)
    description = models.TextField()

    # Link to parent class
    ingredient_class = models.ForeignKey(IngredientClass, related_name='categories', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural: 'ingredient categories'


class IngredientSubcategory(BaseObjectWithImage):
    ''' Sub-category for ingredients (subset of a category) '''
    name = models.CharField(max_length=NAME_LENGTH_SHORT)
    description = models.TextField()

    # Link to parent category
    category = models.ForeignKey(IngredientCategory, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural: 'ingredient subcategories'


# -----------
# MAIN TABLES
# -----------
class Ingredient(BaseObjectWithImage):
    '''
    A single cocktail ingredient, which includes spirits, liqueurs, juices, sweeteners, garnishes, etc.
    '''
    # Information about who makes this and where to buy it
    distillery = models.ForeignKey(
        Distillery,
        related_name='ingredients',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        related_name='ingredients',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    # Bottle information
    average_cost = models.DecimalField(
        decimal_places=2,
        max_digits=7,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    abv = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        null=True,
        blank=True,
    )

    # Ingredients can be classed under each other
    # Ex: Beefeater -> London Dry Gin -> Gin
    subcategory = models.ForeignKey(
        IngredientSubcategory,
        related_name='ingredients',
        null=True,
        on_delete=models.SET_NULL
    )

    def proof(self):
        return self.abv*2.0 or None


class Cocktail(BaseObjectWithImage):
    '''
    High level class for a cocktail. Contains a list of recipes as
    well as general information on the drink.
    '''
    category = models.ForeignKey(CocktailCategory, related_name='cocktails', null=True, on_delete=models.SET_NULL)

    # Base spirit is pulled from the ingredients table
    # base_spirit = models.ForeignKey(Ingredient, )


class Recipe(BaseObjectWithImage):
    '''
    Recipe for a specific cocktail.
    Ideas:
      Base spirit?
      Garnish?
      Cup?
      Hardware?
      Source?
      Ice requirements?
      Shaking type (i.e. shaken, stirred, swizzled, whipped, etc.)
    '''

    # Link to the cokctail object that this is a recipe for
    cocktail = models.ForeignKey(Cocktail, related_name='recipes', on_delete=models.CASCADE)

    # Glassware and hardware
    glassware = models.ForeignKey(Glassware, related_name='recipes', null=True, on_delete=models.SET_NULL)


class RecipeIngredient(models.Model):
    '''
    Line item in a recipe (ingredient + ammount).
    In SQL, this becomes the joining table for the many-to-many relationship.
    '''

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, null=True, on_delete=models.SET_NULL)

    amount = DecimalFractionField(decimal_places=3, max_digits=5)
    unit = models.ForeignKey(UnitOfMeasure, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.recipe.name + ' - ' + self.ingredient.name
