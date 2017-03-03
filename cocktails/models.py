'''
Module: cocktails.models.py

Description: This module contains models necessary to describe
cocktail recipes. This is a hierarchy of objects:

Drink --> Recipe(s) --> Ingredient(s)
'''

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse
from django.db.models.fields.related import ManyToManyField

from django_countries.fields import CountryField
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField

from djfractions.models import DecimalFractionField

from decimal import Decimal
import datetime

# ---------
# Constants
# ---------
NAME_LENGTH_SHORT = 20
NAME_LENGTH_MED = 40
NAME_LENGTH_LONG = 60
URL_LENGTH = 300


# ------------
# Base Objects
# ------------
class BaseObjectWithImage(models.Model):
    ''' Base class that most of the tables share '''
    name = models.CharField(max_length=NAME_LENGTH_LONG, unique=True)
    description = models.TextField(default='', blank=True)

    image_url = models.URLField(
        max_length=URL_LENGTH,
        verbose_name='Image URL',
        null=True,
        blank=True
    )

    wiki_url = models.URLField(
        max_length=URL_LENGTH,
        verbose_name='Wikipedia URL',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name


class BaseObjectAmazon(models.Model):
    ''' Many objects will be purchaseable from Amazon or another site '''
    amazon_url_us = models.URLField(
        max_length=URL_LENGTH,
        verbose_name='Amazon US URL',
        null=True,
        blank=True
    )

    amazon_url_uk = models.URLField(
        max_length=URL_LENGTH,
        verbose_name='Amazon UK URL',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class ToDictMixin(object):
    ''' Adds a method which converts an instance into a dictionary, keeping
    intact many-to-many and non-editable fields
    '''

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(self).values_list('pk', flat=True))
            elif isinstance(f, CountryField):
                data[f.name] = self.country.code
            else:
                data[f.name] = f.value_from_object(self)
        return data


# ----------------
# AUXILIARY TABLES
# ----------------
class UnitOfMeasure(models.Model):
    ''' Units used to measure ingredients in a recipe or glass '''
    name = models.CharField(max_length=NAME_LENGTH_SHORT, unique=True)
    plural = models.CharField(max_length=NAME_LENGTH_SHORT, unique=True)

    class Meta:
        verbose_name_plural = 'units of measure'


class Glassware(BaseObjectWithImage):
    ''' Type of glassware and other cups '''

    # Volume
    volume = models.DecimalField(decimal_places=2, max_digits=5)
    unit = models.ForeignKey(UnitOfMeasure, related_name='glassware', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'glassware'


class Tool(BaseObjectWithImage, BaseObjectAmazon):
    ''' Cocktail hardware (i.e. shakers, spoons, jiggers, etc.) '''
    # What else do we need here besides the description?
    # Brand? Material? Volume?


class PreparationMethod(BaseObjectWithImage):
    ''' Methods that are used to make cocktails '''


class Manufacturer(BaseObjectWithImage):
    ''' Manufaturer of spirits, hardware and other products '''

    # Location
    country = CountryField()
    us_state = USStateField(choices=STATE_CHOICES, verbose_name='state', null=True, blank=True)
    city = models.CharField(max_length=NAME_LENGTH_LONG, null=True, blank=True)

    # Manufacturer's Website
    own_url = models.URLField(
        max_length=URL_LENGTH,
        verbose_name='Own URL',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Distillery(BaseObjectWithImage):
    ''' Location where a spirit is distilled. This is often different than
        the manufacturer since many brands have been bought or have parent
        companies.
    '''

    # Location
    country = CountryField()
    us_state = USStateField(choices=STATE_CHOICES, null=True, blank=True)
    city = models.CharField(max_length=NAME_LENGTH_LONG, null=True, blank=True)

    # Distillery's Website
    own_url = models.URLField(
        max_length=URL_LENGTH,
        verbose_name='Own URL',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'distilleries'

    def __str__(self):
        return self.name


class Brand(ToDictMixin, BaseObjectWithImage):
    ''' Parent object for ingredients, which links out to the distillery
    and manufacturer
    '''

    # Location
    country = CountryField()
    us_state = USStateField(choices=STATE_CHOICES, null=True, blank=True)
    city = models.CharField(max_length=NAME_LENGTH_LONG, null=True, blank=True)

    # Other
    year_established = models.PositiveIntegerField(
        validators=[MaxValueValidator(datetime.datetime.now().year), MinValueValidator(1600)],
    )

    # Distillery and manufacturer
    distillery = models.ForeignKey(
        Distillery,
        related_name='brands',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    manufacturer = models.ForeignKey(
        Manufacturer,
        related_name='brands',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    # Distillery's Website
    own_url = models.URLField(
        max_length=URL_LENGTH,
        verbose_name='Own URL',
        null=True,
        blank=True
    )

    def get_absolute_url(self):
        return reverse('brand-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class CocktailCategory(BaseObjectWithImage):
    ''' Types of cocktails (Flip, fizz, julep, punch, etc.) '''

    class Meta:
        verbose_name_plural = 'cocktail categories'


class IngredientClass(BaseObjectWithImage):
    ''' Umbrella for major ingredient types. Mostly used for sorting
        and differentiating spirits, liqueurs and non-alcoholic ingredients.
    '''

    class Meta:
        verbose_name_plural = 'ingredient classes'

    def get_absolute_url(self):
        return reverse('ingredient-class-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class IngredientCategory(BaseObjectWithImage):
    ''' Major category for ingredients '''

    # Link to parent class
    ingredient_class = models.ForeignKey(IngredientClass, related_name='categories', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'ingredient categories'

    def get_absolute_url(self):
        return reverse('ingredient-category-detail', kwargs={'pk': self.pk})


class IngredientSubcategory(BaseObjectWithImage):
    ''' Sub-category for ingredients (subset of a category) '''

    # Link to parent category
    category = models.ForeignKey(IngredientCategory, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'ingredient subcategories'

    def get_absolute_url(self):
        return reverse('ingredient-subcategory-detail', kwargs={'pk': self.pk})


# -----------
# MAIN TABLES
# -----------
class Ingredient(ToDictMixin, BaseObjectWithImage, BaseObjectAmazon):
    '''
    A single cocktail ingredient, which includes spirits, liqueurs, juices, sweeteners, garnishes, etc.
    '''
    # Information about who makes this and where to buy it
    brand = models.ForeignKey(
        Brand,
        related_name='ingredients',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    # Bottle information
    abv = models.DecimalField(
        decimal_places=1,
        max_digits=5,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        null=True,
        blank=True,
    )

    # Ingredient's website
    own_url = models.URLField(
        max_length=URL_LENGTH,
        verbose_name='Own URL',
        null=True,
        blank=True
    )

    # Ingredients can be classed under each other
    # Ex: Beefeater -> London Dry Gin -> Gin
    subcategory = models.ForeignKey(
        IngredientSubcategory,
        related_name='ingredients',
        null=True,
        on_delete=models.SET_NULL
    )

    def get_absolute_url(self):
        return reverse('ingredient-detail', kwargs={'pk': self.pk})

    def proof(self):
        return self.abv*2.0 or None


class Cocktail(ToDictMixin, BaseObjectWithImage):
    '''
    High level class for a cocktail. Contains a list of recipes as
    well as general information on the drink.
    '''
    category = models.ForeignKey(CocktailCategory, related_name='cocktails', null=True, on_delete=models.SET_NULL)

    # Base spirit is pulled from the ingredients table
    base_spirit = models.ForeignKey(Ingredient, related_name='cocktails', null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('cocktail-detail', kwargs={'pk': self.pk})

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

    # Link to the cocktail object that this is a recipe for
    cocktail = models.ForeignKey(Cocktail, related_name='recipes', on_delete=models.CASCADE)

    # Glassware and hardware
    glassware = models.ForeignKey(Glassware, related_name='recipes', null=True, on_delete=models.SET_NULL)


class RecipeIngredient(models.Model):
    '''
    Line item in a recipe (ingredient + amount).
    In SQL, this becomes the joining table for the many-to-many relationship.
    '''

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, null=True, on_delete=models.SET_NULL)

    amount = DecimalFractionField(decimal_places=3, max_digits=5)
    unit = models.ForeignKey(UnitOfMeasure, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.recipe.name + ' - ' + self.ingredient.name
