from django import template
from django.urls import reverse

register = template.Library()


@register.filter()
def choice_field_name(value, choices):
    ''' Takes a list of choices and finds the name for this value '''
    for key, choice in choices:
        if value == key:
            return choice

    return 'None'


@register.inclusion_tag('snippet_read_only_choice.html')
def read_only_choice(form_field):

    value = 'None'
    for key, choice in form_field.field.choices:
        if form_field.value() == key:
            value = choice

    context = {
        'label': form_field.label,
        'value': value,
        'model_name': form_field.html_name,
        'field': form_field,
    }

    return context


@register.inclusion_tag('snippet_add_field.html')
def add_new_field(form_field, create_url=None):
    ''' Shortcut for adding a label, field and error list '''
    if create_url:
        create_url = reverse(create_url)

    context = {
        'label': form_field.label,
        'form_field': form_field,
        'html_name': form_field.html_name,
        'create_url': create_url,
    }
    return context
