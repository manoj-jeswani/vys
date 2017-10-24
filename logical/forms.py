from django import forms
from django.core.exceptions import ValidationError
from .validators import *
class search_submit_form(forms.Form):
    keyword= forms.CharField(label='', min_length=3, max_length=150)
    
class utube_submit(forms.Form):
    link= forms.CharField(label='', min_length=3, max_length=150,validators=[validate_url])
