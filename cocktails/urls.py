from django.conf.urls import url

from .views import Home
from .views import IngredientDetail, IngredientEdit
from .views import DistilleryEdit, DistilleryDetail
from .views import ManufacturerEdit, ManufacturerDetail
from .views import ingredient_search
from .views import ingredient_cat, ingredient_class_edit, ingredient_category_edit, ingredient_subcategory_edit

urlpatterns = [
    url(r'^$', Home.as_view(), name='cocktail-home'),
    url(r'^ingredient/new/$', IngredientEdit.as_view(), name='ingredient-create'),
    url(r'^ingredient/(?P<pk>\d+)/$', IngredientDetail.as_view(), name='ingredient-detail'),
    url(r'^ingredient/(?P<pk>\d+)/edit/$', IngredientEdit.as_view(), name='ingredient-update'),

    url(r'^ingredient_search/$', ingredient_search, name='ingredient-search'),

    url(r'^distillery/new/$', DistilleryEdit.as_view(), name='distillery-create'),
    url(r'^distillery/(?P<pk>\d+)/$', DistilleryDetail.as_view(), name='distillery-detail'),
    url(r'^distillery/(?P<pk>\d+)/edit/$', DistilleryEdit.as_view(), name='distillery-update'),

    url(r'^manufacturer/new/$', ManufacturerEdit.as_view(), name='manufacturer-create'),
    url(r'^manufacturer/(?P<pk>\d+)/$', ManufacturerDetail.as_view(), name='manufacturer-detail'),
    url(r'^manufacturer/(?P<pk>\d+)/edit/$', ManufacturerEdit.as_view(), name='manufacturer-update'),

    url(r'^ingredient_categorization/$', ingredient_cat, name='ingredient-categorization-browser'),

    url(r'^ingredient_class/new/$', ingredient_class_edit, name='ingredient-class-create'),
    url(r'^ingredient_class/(?P<pk>\d+)/edit/$', ingredient_class_edit, name='ingredient-class-update'),

    url(r'^ingredient_category/new/$', ingredient_category_edit, name='ingredient-category-create'),
    url(r'^ingredient_category/(?P<pk>\d+)/edit/$', ingredient_category_edit, name='ingredient-category-update'),

    url(r'^ingredient_subcategory/new/$', ingredient_subcategory_edit, name='ingredient-subcategory-create'),
    url(r'^ingredient_subcategory/(?P<pk>\d+)/edit/$', ingredient_subcategory_edit, name='ingredient-subcategory-update'),
]
