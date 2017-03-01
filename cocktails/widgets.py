from django import forms
from django.conf import settings
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.utils.html import format_html


class SingleReadOnlyMixin(object):
    ''' This mixin overrides the render method of widgets, adding a <p>
    tag in front that contains the value and a 'readonly-field' class
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
            'id': 'readonly-' + name,
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
            'id': 'readonly-' + name,
            'data-pk': str(value),
        }

        label = 'None'
        for choice_value, choice_label in self.choices:
            if value == choice_value:
                label = choice_label

        return format_html('<p{}>', flatatt(readonly_attrs)) + label + '</p>'


class CreateNewButtonWidget(forms.Widget):
    ''' Widget for a button that creates a new model '''

    def __init__(self, widget, add_url):
        self.widget = widget
        self.attrs = widget.attrs
        self.choices = widget.choices
        self.needs_multipart_form = widget.needs_multipart_form
        self.add_url = add_url + '?_popup=1'

    def render(self, name, value, *args, **kwargs):
        # Render the widget we are wrapping
        output = [self.widget.render(name, value, *args, **kwargs)]

        # Add a link and the plus icon after the widget
        output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showRelatedObjectPopup(this);">'
                      % (self.add_url, name))
        output.append(u'<img src="%sadmin/img/icon-addlink.svg" width="10" height="10" alt="%s" />'
                      % (settings.STATIC_URL, 'Create New Item'))
        output.append(u'</a>')

        return mark_safe(u''.join(output))

    @property
    def is_hidden(self):
        return self.widget.is_hidden

    @property
    def media(self):
        return self.widget.media
