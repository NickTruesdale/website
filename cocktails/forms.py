from django import forms
from .models import Ingredient


class IngredientForm(forms.ModelForm):
    ''' Form for adding and editing ingredients '''

    class Meta:
        model = Ingredient
        fields = (
            'name',
            'description',
            'image_url',
            'own_url',
            'wiki_url',
            'amazon_url_us',
            'amazon_url_uk',
            'subcategory',
            'distillery',
            'manufacturer',
            'abv',
        )
