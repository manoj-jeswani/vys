from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

def validate_url(value):
	url_validator=URLValidator()
	new_val=''
	if 'http' in value:
		new_val=value
	else:
		new_val='http://'+value

	try:
		url_validator(new_val)
	except:
		raise ValidationError('Invalid URL')
	
	return new_val