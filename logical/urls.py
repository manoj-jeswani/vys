from django.conf.urls import url
from .views import *

urlpatterns = [

	url(r'^$',index_get_query, name='index_g'),
	url(r'^search-results/(?P<v_id>[-\w]+)/(?P<d_audio>\d+)$',index_show_results, name='index_s'),
	


]