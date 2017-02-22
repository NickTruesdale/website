from django.conf.urls import url

from .views import Home
from .views import IngredientDetail, IngredientEdit
from .views import IngredientCategoryEdit, IngredientCategoryDetail
from .views import IngredientClassEdit, IngredientClassDetail
from .views import IngredientSubcategoryEdit, IngredientSubcategoryDetail
from .views import DistilleryEdit, DistilleryDetail
from .views import ManufacturerEdit, ManufacturerDetail
from .views import IngredientCategorization

urlpatterns = [
    url(r'^$', Home.as_view(), name='cocktail-home'),
    url(r'^ingredient/new/$', IngredientEdit.as_view(), name='ingredient-create'),
    url(r'^ingredient/(?P<pk>\d+)/$', IngredientDetail.as_view(), name='ingredient-detail'),
    url(r'^ingredient/(?P<pk>\d+)/edit/$', IngredientEdit.as_view(), name='ingredient-update'),

    url(r'^ingredient_class/new/$', IngredientClassEdit.as_view(), name='ingredient-class-create'),
    url(r'^ingredient_class/(?P<pk>\d+)/$', IngredientClassDetail.as_view(), name='ingredient-class-detail'),
    url(r'^ingredient_class/(?P<pk>\d+)/edit/$', IngredientClassEdit.as_view(), name='ingredient-class-update'),

    url(r'^ingredient_category/new/$', IngredientCategoryEdit.as_view(), name='ingredient-category-create'),
    url(r'^ingredient_category/(?P<pk>\d+)/$', IngredientCategoryDetail.as_view(), name='ingredient-category-detail'),
    url(r'^ingredient_category/(?P<pk>\d+)/edit/$', IngredientCategoryEdit.as_view(), name='ingredient-category-update'),

    url(r'^ingredient_subcategory/new/$', IngredientSubcategoryEdit.as_view(), name='ingredient-subcategory-create'),
    url(r'^ingredient_subcategory/(?P<pk>\d+)/$', IngredientSubcategoryDetail.as_view(), name='ingredient-subcategory-detail'),
    url(r'^ingredient_subcategory/(?P<pk>\d+)/edit/$', IngredientSubcategoryEdit.as_view(), name='ingredient-subcategory-update'),

    url(r'^distillery/new/$', DistilleryEdit.as_view(), name='distillery-create'),
    url(r'^distillery/(?P<pk>\d+)/$', DistilleryDetail.as_view(), name='distillery-detail'),
    url(r'^distillery/(?P<pk>\d+)/edit/$', DistilleryEdit.as_view(), name='distillery-update'),

    url(r'^manufacturer/new/$', ManufacturerEdit.as_view(), name='manufacturer-create'),
    url(r'^manufacturer/(?P<pk>\d+)/$', ManufacturerDetail.as_view(), name='manufacturer-detail'),
    url(r'^manufacturer/(?P<pk>\d+)/edit/$', ManufacturerEdit.as_view(), name='manufacturer-update'),

    url(r'^ingredient_categorization/$', IngredientCategorization.as_view(), name='ingredient-categorization-browser')
]
