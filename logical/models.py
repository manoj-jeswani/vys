import json
from django.core.serializers.json import DjangoJSONEncoder

from django.db import models
from collections import OrderedDict
# Create your models here.

from django.conf import settings

#from settings file get value of SHORTCODE_MAX and if is not present then return 15
SHORTCODE_MAX=getattr(settings,"SHORTCODE_MAX",15)


class Uploadmp4(models.Model):
    code=models.CharField(max_length=SHORTCODE_MAX,unique=True,blank=True)

    up = models.FileField(upload_to='videouploads/')
    # uploaded_at = models.DateTimeField(auto_now_add=True)
   

class TemporaryDetails(models.Model):
	title=models.CharField(max_length=250,blank=False)
	v_id=models.CharField(max_length=250,blank=False)
	d_audio=models.IntegerField(blank=False)



class JSONField(models.TextField):
    """
    JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly.
    Django snippet #1478

    example:
        class Page(models.Model):
            data = JSONField(blank=True, null=True)


        page = Page.objects.get(pk=5)
        page.data = {'title': 'test', 'type': 3}
        page.save()
    """

    def to_python(self, value):
        if value == "":
            return None

        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass
        return value

    def from_db_value(self, value, *args):
        return self.to_python(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, list):
            value = json.dumps(value, cls=DjangoJSONEncoder)
        return value




class Search_Result(models.Model):
	kw=models.CharField(max_length=250,blank=True)
	sres=JSONField(blank=True, null=True)


'''
JSONField
OrderedDict

https://stackoverflow.com/questions/9686409/how-to-store-a-dictionary-in-a-django-database-models-field

https://stackoverflow.com/questions/5629023/key-order-in-python-dictionaries

https://stackoverflow.com/questions/10844064/items-in-json-object-are-out-of-order-using-json-dumps

'''