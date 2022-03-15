from django import forms
from django.forms.widgets import URLInput

class UrlForm(forms.Form):
    url = forms.URLField(label='URL', widget= URLInput)

    class Meta:
        fields = ['URL']