from django import forms
from django.conf import settings
from django.urls import reverse

from .models import Ingredient, IngredientClass, IngredientCategory, IngredientSubcategory
from .models import Distillery, Manufacturer
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

        # Populate the class and category fields
        if self.instance:
            category = self.instance.subcategory.category
            self.fields['ingredient_category'].initial = category
            self.fields['ingredient_class'].initial = category.ingredient_class

        # Sort ModelChoiceFields alphabetically
        self.fields['manufacturer'].choices = sorted(
            self.fields['manufacturer'].choices,
            key=lambda x: x[1]
        )

        self.fields['distillery'].choices = sorted(
            self.fields['distillery'].choices,
            key=lambda x: x[1]
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
        widgets = {
          'description': forms.Textarea(attrs={'rows': 4}),
        }


class IngredientSearchForm(forms.Form):
    ''' Form containing model selects for each FK field in ingredient '''
    name = forms.CharField(max_length=60)

    ingredient_class = forms.ModelChoiceField(
        queryset=IngredientClass.objects.all(),
    )

    ingredient_category = forms.ModelChoiceField(
        queryset=IngredientCategory.objects.all(),
    )

    ingredient_subcategory = forms.ModelChoiceField(
        queryset=IngredientSubcategory.objects.all(),
    )

    distillery = forms.ModelChoiceField(
        queryset=Distillery.objects.all(),
    )

    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(),
    )
