from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import escape, escapejs
from django.http import HttpResponse

from .models import Ingredient, IngredientSubcategory, IngredientCategory, IngredientClass
from .forms import IngredientForm, IngredientClassForm, IngredientCategoryForm


# Create your views here.
def cocktail_home(request):
    ''' Default landing page for now '''
    return render(request, 'cocktails/home.html')


def ingredient_new(request):
    ''' View for new ingredients '''

    # Check if we're getting a POSTed form, otherwise make a blank new one
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.save()
            return redirect('ingredient_detail', pk=ingredient.pk)
    else:
        form = IngredientForm()

    return render(request, 'cocktails/ingredient_edit.html', {'form': form})


def ingredient_edit(request, pk):
    ''' View for editing an existing ingredient '''
    # Make sure this PK points to a valid ingredient
    ingredient = get_object_or_404(Ingredient, pk=pk)

    # Validate a POSTed form or render a new one using this ingredient
    if request.method == "POST":
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.save()
            return redirect('ingredient_detail', pk=ingredient.pk)

    else:
        form = IngredientForm(instance=ingredient)

    return render(request, 'cocktails/ingredient_edit.html', {'form': form})


def ingredient_detail(request, pk):
    ''' View for a single ingredient '''
    ingredient = get_object_or_404(Ingredient, pk=pk)
    return render(request, 'cocktails/ingredient_detail.html', {'ingredient': ingredient})


def ingredient_category_new(request):
    ''' Form for adding a new category for ingredients '''
    # On POST, we need to validate, then either redirect (if in the main window)
    # or send back to the original window (if in a popup)
    context = {}
    if request.method == "POST":
        form = IngredientCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            if "_popup" in request.POST:
                response = '<script type="text/javascript">'
                response += 'opener.dismissAddAnotherPopup(window, "%s", "%s");' \
                    % (escape(category.pk), escapejs(category))
                response += '</script>'
                return HttpResponse(response)
            else:
                return redirect('ingredient_detail', pk=1)

    # When the form opens, we get a blank instance and
    # check whether this is a popup window or not
    else:
        form = IngredientCategoryForm()
        if '_popup' in request.GET:
            context['popup'] = 1

    context['form'] = form
    return render(request, 'cocktails/ingredient_category_new.html', context)


# -------------------
# Generic Model Forms
# -------------------
class IngredientCategoryCreate(CreateView):
    model = IngredientCategory
    fields = ['name', 'description', 'ingredient_class', 'image_url', 'wiki_url']


