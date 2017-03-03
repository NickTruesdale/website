from django import forms
from django.forms.utils import flatatt
from django.utils.html import format_html

from django_countries.widgets import CountrySelectWidget


class SingleReadOnlyMixin(object):
    ''' This mixin overrides the render method of widgets, adding a <p>
    tag in front that contains the value and a 'readonly-field' class.
    It also adds the 'editable-field' class to the default widget. These
    can be used together to toggle between readonly and edit modes.
    '''

    def render(self, name, value, attrs=None):
        # Add class to input field
        if attrs is None:
            attrs = {}
        attrs['class'] = 'editable-field'

        # Create the additional HTML and put it in front
        output = [self.create_output(name, value)]
        output.append(super().render(name, value, attrs))
        return '\n'.join(output)

    def create_output(self, name, value):
        readonly_attrs = {
            'class': 'readonly-field',
            'id': 'readonly_' + name,
        }
        return format_html('<p{}>', flatatt(readonly_attrs)) + str(value) + '</p>'


class InputWithReadOnly(SingleReadOnlyMixin, forms.widgets.TextInput):
    ''' Add a read-only field to an TextInput '''
    pass


class TextareaWithReadOnly(SingleReadOnlyMixin, forms.widgets.Textarea):
    ''' Add a read-only field to an TextArea '''
    pass


class SelectWithReadOnly(SingleReadOnlyMixin, forms.widgets.Select):
    ''' This overrides the Select widget to have an additional text field '''

    def create_output(self, name, value):
        readonly_attrs = {
            'class': 'readonly-field',
            'id': 'readonly_' + name,
            'data-pk': str(value),
        }

        label = 'None'
        for choice_value, choice_label in self.choices:
            if value == choice_value:
                label = choice_label

        return format_html('<p{}>', flatatt(readonly_attrs)) + label + '</p>'


class CountrySelectWithReadOnly(SingleReadOnlyMixin, CountrySelectWidget):
    ''' This overrides the CountrySelect widget to have an additional text field '''

    def create_output(self, name, value):
        readonly_attrs = {
            'class': 'readonly-field',
            'id': 'readonly_' + name,
            'data-pk': str(value),
        }

        label = 'None'
        for choice_value, choice_label in self.choices:
            if value == choice_value:
                label = choice_label

        return format_html('<p{}>', flatatt(readonly_attrs)) + label + '</p>'
