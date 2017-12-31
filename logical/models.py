from django.db import models

# Create your models here.

from django.conf import settings

#from settings file get value of SHORTCODE_MAX and if is not present then return 15
SHORTCODE_MAX=getattr(settings,"SHORTCODE_MAX",15)


class Uploadmp4(models.Model):
    code=models.CharField(max_length=SHORTCODE_MAX,unique=True,blank=True)

    up = models.FileField(upload_to='videouploads/')
    # uploaded_at = models.DateTimeField(auto_now_add=True)
   

