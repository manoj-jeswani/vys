from django.shortcuts import render
from .forms import FeedbackForm,QueryForm
import json
from django.http import HttpResponse
# Create your views here.


def FeedbackView(request):
	if request.method=='POST':
		response = {}
		
		f=FeedbackForm(request.POST)
		if f.is_valid():
			f.save()
			if request.is_ajax():
				response['valid']=True
				response['message'] = "Feedback Submitted..Thanks for lending us your time."
		else:
			if request.is_ajax():
				response['valid']=False
				response['message'] = "Unable to submit, verify the entries and submit again.. "
	else:
		if request.is_ajax():
			response['message'] = "No Feedback submitted..(GET request)"


	return HttpResponse(json.dumps(response), content_type ='application/json; charset=utf8')




				

	

def QueryView(request):
	if request.method=='POST':
		response = {}
		
		f=QueryForm(request.POST)
		if f.is_valid():
			f.save()
			if request.is_ajax():
				response['valid']=True
				response['message'] = "Query Submitted..We will get back to you asap."
		else:
			if request.is_ajax():
				response['valid']=False
				response['message'] = "Unable to submit, verify the entries and submit again.. "
	else:
		if request.is_ajax():
			response['message'] = "No Query submitted..(GET request)"


	return HttpResponse(json.dumps(response), content_type ='application/json; charset=utf8')




