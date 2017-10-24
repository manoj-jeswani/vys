from django.conf.urls import url
from .views import *

urlpatterns = [

	url(r'^cnv$',cn_view, name='cnv'),

	url(r'^yvd$',yv_view, name='yvd'),
	url(r'^$',index_view, name='index_home'),
	
	url(r'^omp3$',mp3_get_query, name='index_g'),
	url(r'^omp3/search-results/(?P<v_id>[-\w]+)/(?P<d_audio>\d+)$',mp3_show_results, name='index_s'),
	


]