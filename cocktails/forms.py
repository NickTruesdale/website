from django import forms
from django.conf import settings
from django.urls import reverse

from .models import Ingredient, IngredientClass, IngredientCategory, IngredientSubcategory
from .widgets import CreateNewButtonWidget


# ----------------------
# INGREDIENT FORM WIZARD
# -----------------------
class IngredientPreForm1(forms.ModelForm):
    ''' Simple form for adding a class to a category '''

    class Meta:
        model = IngredientCategory
        fields = ('ingredient_class',)


class IngredientPreForm2(forms.ModelForm):
    ''' After choosing a class, the user chooses a category '''

    class Meta:
        model = IngredientSubcategory
        fields = ('category',)


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
        self.fields['ingredient_category'].widget = CreateNewButtonWidget(
            self.fields['ingredient_category'].widget,
            reverse('ingredient_category_new')
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


class IngredientCategoryForm(forms.ModelForm):

    class Media:
        js = (
            settings.STATIC_URL + 'admin/js/admin/RelatedObjectLookups.js',
        )

    class Meta:
        model = IngredientCategory
        fields = (
            'name',
            'description',
            'image_url',
            'wiki_url',
            'ingredient_class',
        )


class IngredientClassForm(forms.ModelForm):

    class Meta:
        model = IngredientClass
        fields = (
            'name',
            'description',
            'image_url',
            'wiki_url',
        )
