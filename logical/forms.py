from django import forms
from django.core.exceptions import ValidationError
from .validators import *
from .models import Uploadmp4

class search_submit_form(forms.Form):
    keyword= forms.CharField(label='', min_length=3, max_length=150)
    
class utube_submit(forms.Form):
    link= forms.CharField(label='', min_length=3, max_length=150,validators=[validate_url])




class Uploadmp4Form(forms.ModelForm):
    class Meta:
        model = Uploadmp4
        exclude = ("code",)
