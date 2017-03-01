from django import forms
from django.conf import settings
from django.urls import reverse

from .models import Ingredient, IngredientClass, IngredientCategory, IngredientSubcategory
from .models import Distillery, Manufacturer
from .widgets import InputWithReadOnly, TextareaWithReadOnly, SelectWithReadOnly


# ---------------
# INGREDIENT FORM
# ---------------
class IngredientForm(forms.ModelForm):
    ''' Form for adding and editing ingredients '''

    # Fields for class and category
    ingredient_class = forms.ModelChoiceField(
        queryset=IngredientClass.objects.all(),
        widget=SelectWithReadOnly,
    )

    ingredient_category = forms.ModelChoiceField(
        queryset=IngredientCategory.objects.all(),
        widget=SelectWithReadOnly,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print(self.fields['name'].widget.attrs)
        for key, value in self.fields['name'].widget.attrs.items():
            print('%s - %s', (key, value))

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
            'subcategory': SelectWithReadOnly(),
            'distillery': SelectWithReadOnly(),
            'manufacturer': SelectWithReadOnly(),
            'name': InputWithReadOnly(),
            'description': TextareaWithReadOnly(attrs={'rows': 4}),
            'image_url': InputWithReadOnly(),
            'abv':  InputWithReadOnly(),
            'own_url': InputWithReadOnly(),
            'wiki_url': InputWithReadOnly(),
            'amazon_url_us': InputWithReadOnly(),
            'amazon_url_uk': InputWithReadOnly(),
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
