from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe


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
