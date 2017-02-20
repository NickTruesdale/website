from django import forms
from django.conf import settings
from django.urls import reverse

from .models import Ingredient, IngredientClass, IngredientCategory
from .widgets import CreateNewButtonWidget


# ---------------
# INGREDIENT FORM
# ---------------
class IngredientForm(forms.ModelForm):
    ''' Form for adding and editing ingredients '''

    # Fields for class and category
    ingredient_class = forms.ModelChoiceField(
        queryset=IngredientClass.objects.all(),
    )

    ingredient_category = forms.ModelChoiceField(
        queryset=IngredientCategory.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create custom wrapper widgets for the Foreign Key fields
        self.fields['ingredient_class'].widget = CreateNewButtonWidget(
            self.fields['ingredient_class'].widget,
            reverse('ingredient-class-create')
        )
        self.fields['ingredient_category'].widget = CreateNewButtonWidget(
            self.fields['ingredient_category'].widget,
            reverse('ingredient-category-create')
        )
        self.fields['subcategory'].widget = CreateNewButtonWidget(
            self.fields['subcategory'].widget,
            reverse('ingredient-subcategory-create')
        )
        self.fields['distillery'].widget = CreateNewButtonWidget(
            self.fields['distillery'].widget,
            reverse('distillery-create')
        )
        self.fields['manufacturer'].widget = CreateNewButtonWidget(
            self.fields['manufacturer'].widget,
            reverse('manufacturer-create')
        )

    class Media:
        css = {'all': (settings.STATIC_URL + 'admin/css/widgets.css',)}
        js = (
            settings.STATIC_URL + 'admin/js/admin/RelatedObjectLookups.js',
        )

    class Meta:
        model = Ingredient
        fields = (
            'ingredient_class',
            'ingredient_category',
            'subcategory',
            'name',
            'description',
            'image_url',
            'distillery',
            'manufacturer',
            'abv',
            'own_url',
            'wiki_url',
            'amazon_url_us',
            'amazon_url_uk',
        )
