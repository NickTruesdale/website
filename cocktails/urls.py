from django.conf.urls import url
from django.views.generic.base import RedirectView

from .views import Home
from .views import ingredient_detail
from .views import ingredient_cat, ingredient_class_edit, ingredient_category_edit, ingredient_subcategory_edit
from .views import brand_detail, distillery_edit, manufacturer_edit
from .views import cocktail_detail, cocktail_category_edit

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=False)

urlpatterns = [
    url(r'^$', Home.as_view(), name='cocktail-home'),

    url(r'^cocktail/new/$', cocktail_detail, name='cocktail-create'),
    url(r'^cocktail/(?P<pk>\d+)/$', cocktail_detail, name='cocktail-detail'),
    url(r'^cocktail/(?P<pk>\d+)/edit/$', cocktail_detail, name='cocktail-update'),

    url(r'^cocktail_category/new/$', cocktail_category_edit, name='cocktail-category-create'),
    url(r'^cocktail_category/(?P<pk>\d+)/edit/$', cocktail_category_edit, name='cocktail-category-update'),

    url(r'^ingredient/new/$', ingredient_detail, name='ingredient-create'),
    url(r'^ingredient/(?P<pk>\d+)/$', ingredient_detail, name='ingredient-detail'),
    url(r'^ingredient/(?P<pk>\d+)/edit/$', ingredient_detail, name='ingredient-update'),

    url(r'^brand/new/$', brand_detail, name='brand-create'),
    url(r'^brand/(?P<pk>\d+)/$', brand_detail, name='brand-detail'),
    url(r'^brand/(?P<pk>\d+)/edit/$', brand_detail, name='brand-update'),

    url(r'^ingredient_categorization/$', ingredient_cat, name='ingredient-categorization-browser'),

    url(r'^distillery/new/$', distillery_edit, name='distillery-create'),
    url(r'^distillery/(?P<pk>\d+)/edit/$', distillery_edit, name='distillery-update'),

    url(r'^manufacturer/new/$', manufacturer_edit, name='manufacturer-create'),
    url(r'^manufacturer/(?P<pk>\d+)/edit/$', manufacturer_edit, name='manufacturer-update'),

    url(r'^ingredient_class/new/$', ingredient_class_edit, name='ingredient-class-create'),
    url(r'^ingredient_class/(?P<pk>\d+)/edit/$', ingredient_class_edit, name='ingredient-class-update'),

    url(r'^ingredient_category/new/$', ingredient_category_edit, name='ingredient-category-create'),
    url(r'^ingredient_category/(?P<pk>\d+)/edit/$', ingredient_category_edit, name='ingredient-category-update'),

    url(r'^ingredient_subcategory/new/$', ingredient_subcategory_edit, name='ingredient-subcategory-create'),
    url(r'^ingredient_subcategory/(?P<pk>\d+)/edit/$', ingredient_subcategory_edit, name='ingredient-subcategory-update'),

    url(r'favicon.ico$', favicon_view, name="favicon"),
]
