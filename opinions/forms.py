from django import forms
from django.core.exceptions import ValidationError
from .models import Feedback,Query


class FeedbackForm(forms.ModelForm):
	class Meta:
		model=Feedback
		fields=('name','feed','rating')



class QueryForm(forms.ModelForm):
	class Meta:
		model=Query
		fields=('name','email','issue')
