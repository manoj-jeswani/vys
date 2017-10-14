from django import forms
from django.core.exceptions import ValidationError

class search_submit_form(forms.Form):
    keyword= forms.CharField(label='', min_length=3, max_length=150)
    