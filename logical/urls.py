from django.conf.urls import url
from .views import *

urlpatterns = [

	url(r'^cnv$',cn_view, name='cnv'),

	url(r'^yvd/(?P<a>\d+)$',yv_view, name='yvd'),
	url(r'^$',index_view, name='index_home'),
	url(r'^omp3$',mp3_get_query, name='index_g'),
	url(r'^omp3/search-results$',mp3_show_results, name='index_s'),
	url(r'^load/(?P<v_id>[-\w]+)/(?P<d_audio>\d+)$',load_view, name='load'),

	url(r'^load-status$',load_state, name='load-status'),
	url(r'^get-link$',get_file_link, name='get-link'),

	url(r'^log-search-result$',log_search_result_view, name='lsr'),

	
]