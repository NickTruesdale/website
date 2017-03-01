from django.views.generic import TemplateView, UpdateView, DetailView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import escape, escapejs
from django.apps import apps
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django import forms

from .models import Ingredient, IngredientSubcategory, IngredientCategory, IngredientClass
from .models import Distillery, Manufacturer
from .forms import IngredientForm, IngredientSearchForm


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


class JsonFormMixin(object):
    ''' This mixin provides Json responses for the form_valid and form_invalid
    methods, allowing forms to be posted asynchronously.
    '''

    def get(self, request, *args, **kwargs):
        ''' If the GET request has parameters corresponding to model properties,
        we will try to preload the form with the correct value
        '''
        self.object = self.get_object()
        form_class = self.get_form_class()

        if self.object is None:
            # Grab any valid initial values from the GET params
            initial = {}
            for key, value in request.GET.items():
                if hasattr(self.model, key):
                    initial[key] = value

            form = form_class(initial=initial)
        else:
            form = self.get_form(form_class)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        ''' Return a JSON response with the pk and a success message '''
        instance = form.save()
        response = {'success': 1, 'pk': instance.pk}
        return JsonResponse(response)

    def form_invalid(self, form):
        response = {'success': 0, 'errors': form.errors}
        return JsonResponse(response)

    def verbose_name(self):
        return self.model._meta.verbose_name.title()


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


class IngredientModalView(CreateUpdateMixin, ShortDescriptionMixin, JsonFormMixin, UpdateView):
    ''' Single class which handle the mixins using the modal edit form '''
    template_name = 'cocktails/modal_edit_form.html'


# ---------
# Home page
# ---------
class Home(TemplateView):
    template_name = 'cocktails/home.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            response = []

            model_type = request.GET.get('model')
            search_text = request.GET.get('search_text')

            model = apps.get_model('cocktails', model_type)
            query = model.objects.filter(name__contains=search_text)

            for item in query:
                D = item.to_dict()
                D['detail_url'] = item.get_absolute_url()
                response.append(D)

            return JsonResponse(response, safe=False)
        else:
            return super().get(request, *args, **kwargs)


# ----------
# Ingredient
# ----------
class IngredientDetail(CreateUpdateMixin, UpdateView):
    model = Ingredient
    template_name = 'cocktails/ingredient_detail.html'
    form_class = IngredientForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form

    def form_valid(self, form):
        ''' Return a JSON response with the pk and a success message '''
        instance = form.save()
        response = {'success': 1, 'pk': instance.pk}
        return JsonResponse(response)

    def form_invalid(self, form):
        response = {'success': 0, 'errors': form.errors}
        return JsonResponse(response)


class IngredientEdit(IngredientModalView):
    model = Ingredient
    form_class = IngredientForm


# ------------------------
# Ingredient Field Classes
# ------------------------
class IngredientCategorization(TemplateView):
    ''' This view provides a single interface for looking up ingredient class,
    category and subcategory.

    At initial load, it provides a list of all classes (which in turn can be
    queried for all categories and subcategories)

    It also responds to AJAX GET requests to serve up a
    given instance of one of the three classes for viewing.
    '''

    template_name = 'cocktails/ingredient_categorization_browser.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredientclasses'] = IngredientClass.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            status = 200
            pk = request.GET.get('pk')
            model_type = request.GET.get('model_type')

            try:
                model = apps.get_model('cocktails', model_type)
                response = serializers.serialize('json', model.objects.filter(pk=pk), use_natural_foreign_keys=False)

            except Exception as e:
                status = 400
                response = [{'error_name': type(e).__name__, 'error-text': str(e)}]

            return HttpResponse(response, content_type="application/json", status=status)
        else:
            return super().get(request, *args, **kwargs)


class IngredientClassEdit(IngredientModalView):
    model = IngredientClass
    fields = ['name', 'description', 'image_url', 'wiki_url']


class IngredientCategoryEdit(IngredientModalView):
    model = IngredientCategory
    fields = ['name', 'ingredient_class', 'description', 'image_url', 'wiki_url']


class IngredientSubcategoryEdit(IngredientModalView):
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


# ---------------
# Class Instances
# ---------------
ingredient_cat = IngredientCategorization.as_view()
ingredient_class_edit = IngredientClassEdit.as_view()
ingredient_category_edit = IngredientCategoryEdit.as_view()
ingredient_subcategory_edit = IngredientSubcategoryEdit.as_view()
