from django import template
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
