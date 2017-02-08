from django.shortcuts import render, get_object_or_404

from .models import Ingredient


# Create your views here.
def cocktail_home(request):
    ''' Default landing page for now '''
    return render(request, 'cocktails/home.html')


def ingredient_detail(request, primary_key):
    ''' View for a single ingredient '''
    ingredient = get_object_or_404(Ingredient, pk=primary_key)
    return render(request, 'cocktails/ingredient_detail.html', {'ingredient': ingredient})
