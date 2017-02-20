from django.views.generic import UpdateView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import escape, escapejs
from django.http import HttpResponse
from django import forms

from .models import Ingredient, IngredientSubcategory, IngredientCategory, IngredientClass
from .models import Distillery, Manufacturer
from .forms import IngredientForm


# Create your views here.
def cocktail_home(request):
    ''' Default landing page for now '''
    return render(request, 'cocktails/home.html')


def ingredient_create(request):
    ''' View for new ingredients '''

    # Check if we're getting a POSTed form, otherwise make a blank new one
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.save()
            return redirect('ingredient-detail', pk=ingredient.pk)
    else:
        form = IngredientForm()

    return render(request, 'cocktails/ingredient_edit.html', {'form': form})


def ingredient_update(request, pk):
    ''' View for editing an existing ingredient '''
    # Make sure this PK points to a valid ingredient
    ingredient = get_object_or_404(Ingredient, pk=pk)

    # Validate a POSTed form or render a new one using this ingredient
    if request.method == "POST":
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.save()
            return redirect('ingredient-detail', pk=ingredient.pk)

    else:
        form = IngredientForm(instance=ingredient)

    return render(request, 'cocktails/ingredient_edit.html', {'form': form})


def ingredient_detail(request, pk):
    ''' View for a single ingredient '''
    ingredient = get_object_or_404(Ingredient, pk=pk)
    return render(request, 'cocktails/ingredient_detail.html', {'ingredient': ingredient})


# -----------------------
# Class Based View Mixins
# -----------------------

class CreateUpdateMixin(object):
    ''' Hybrid create/update view. The get_object function is overloaded
    to return None when there is no valid object (i.e. for the Create form).
    A side effect is that, if pk returns an invalid object, the create form
    will show up instead of a 404 page.
    '''

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None


class PopupEditMixin(object):
    ''' This mixin overrides the get_context_data and post methods in order
    to support opening and saving popup forms in the style of the Django admin.
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = self.model._meta.verbose_name.title()
        if '_popup' in self.request.GET:
            context['popup'] = self.request.GET['_popup']
        return context

    def post(self, request, *args, **kwargs):
        post_result = super().post(request, *args, **kwargs)

        if '_popup' in request.POST:
            response = '<script type="text/javascript">'
            response += 'opener.dismissAddAnotherPopup(window, "%s", "%s");' \
                % (escape(self.object.pk), escapejs(self.object))
            response += '</script>'
            return HttpResponse(response)
        else:
            return post_result


class ShortDescriptionMixin(object):
    ''' This mixin shortens the widget for the description field's Textarea '''

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'description' in form.fields:
            form.fields['description'].widget = forms.Textarea(attrs={'rows': 2})
        return form


class IngredientForeignKeyView(CreateUpdateMixin, PopupEditMixin, ShortDescriptionMixin, UpdateView):
    ''' Single class which handles mixins for all child classes that use an edit popup '''
    template_name = 'cocktails/ingredient_foreign_key_edit.html'


# ------------------------
# Ingredient Field Classes
# ------------------------
class IngredientCategoryDetail(DetailView):
    model = IngredientCategory


class IngredientCategoryEdit(IngredientForeignKeyView):
    model = IngredientCategory
    fields = ['name', 'ingredient_class', 'description', 'image_url', 'wiki_url']


class IngredientClassDetail(DetailView):
    model = IngredientClass


class IngredientClassEdit(IngredientForeignKeyView):
    model = IngredientClass
    fields = ['name', 'description', 'image_url', 'wiki_url']


class IngredientSubcategoryDetail(DetailView):
    model = IngredientSubcategory


class IngredientSubcategoryEdit(IngredientForeignKeyView):
    model = IngredientSubcategory
    fields = ['name', 'category', 'description', 'image_url', 'wiki_url']


class DistilleryDetail(DetailView):
    model = Distillery


class DistilleryEdit(IngredientForeignKeyView):
    model = Distillery
    fields = ['name', 'description', 'country', 'us_state', 'city', 'image_url', 'wiki_url', 'own_url']


class ManufacturerDetail(DetailView):
    model = Manufacturer


class ManufacturerEdit(IngredientForeignKeyView):
    model = Manufacturer
    fields = ['name', 'description', 'country', 'us_state', 'city', 'image_url', 'wiki_url', 'own_url']
