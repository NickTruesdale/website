from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cocktail_home, name='cocktail_home'),
    url(r'^ingredient/new/$', views.ingredient_new, name='ingredient_new'),
    url(r'^ingredient/(?P<pk>\d+)/$', views.ingredient_detail, name='ingredient_detail'),
    url(r'^ingredient/(?P<pk>\d+)/edit/$', views.ingredient_edit, name='ingredient_edit'),
    url(r'^ingredient_category/new$', views.ingredient_category_new, name='ingredient_category_new'),
]
