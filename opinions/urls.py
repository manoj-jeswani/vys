from django.conf.urls import url
from .views import *

urlpatterns = [

	url(r'^ufeed$',FeedbackView, name='ufeed'),

	url(r'^uquery$',QueryView, name='uquery'),
	


]