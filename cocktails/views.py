from django.shortcuts import render, get_object_or_404

from .models import Ingredient
from .forms import IngredientForm

# Create your views here.
def cocktail_home(request):
    ''' Default landing page for now '''
    return render(request, 'cocktails/home.html')


def ingredient_detail(request, pk):
    ''' View for a single ingredient '''
    ingredient = get_object_or_404(Ingredient, pk=pk)
    return render(request, 'cocktails/ingredient_detail.html', {'ingredient': ingredient})


def ingredient_new(request):
    ''' View for new ingredients '''
    form = IngredientForm()
    return render(request, 'cocktails/ingredient_edit.html', {'form': form})
