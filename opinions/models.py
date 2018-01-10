from django.db import models
from django.core.validators import validate_email,MinLengthValidator

# Create your models here.

ch=((0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'))


class Feedback(models.Model):
	name=models.CharField(max_length=100,blank=False,validators=[MinLengthValidator(3)])
	feed=models.TextField(max_length=5000,blank=False,validators=[MinLengthValidator(3)])
	rating=models.IntegerField(choices=ch,blank=False)
	create_date = models.DateTimeField(auto_now_add=True)
 


class Query(models.Model):
	name=models.CharField(max_length=100,blank=False,validators=[MinLengthValidator(3)])
	email = models.EmailField(max_length=254, blank=False, validators=[validate_email])
	issue=models.TextField(max_length=5000,blank=False,validators=[MinLengthValidator(3)])
	create_date = models.DateTimeField(auto_now_add=True)
    