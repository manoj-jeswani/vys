import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from logical.download import *
from logical.search import *

from celery import task

@task
def load_item(v_id,d_audio,tempd):

	mm=dload(str(v_id),int(d_audio),tempd)

	return True


@task
def wait_for_thread():
	
	return True




@task
def load_search(kw):
	otpt=search_keyword(str(kw))
	return True


