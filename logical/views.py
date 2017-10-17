from django.shortcuts import render
from .forms import *
from .search import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect
from .download import *



# Create your views here.
def index_get_query(request):
	kw=""
	error_msg=""
	res_list=[]
	res=[]
	if request.method=='POST':
		
		f=search_submit_form(request.POST)
		if f.is_valid():
			kw=f.cleaned_data.get('keyword')
		if kw=="":
			error_msg=f.errors.get('keyword')
			f.errors['keyword']=""
		else:
			res_list=search_keyword(str(kw))
			tempd={}
			tempd['all']="_"
			for i in res_list:
				tempd[i['v_id']]=i['title']

			request.session['results']=res_list
			request.session['tempd']=tempd
			
			return HttpResponseRedirect('search-results/all/8')

			# for i in res_list:
			# 	print(i)

	else:
		f=search_submit_form()
	context={
		"form":f,
		"error_msg":error_msg,
		"kw":kw,
		"res":res,
		}

	return render(request, 'logical/index.html',context)


def uconvert(title):
	res=""
	for i in title:
		if ord(i) in range(ord('A'),ord('Z')+1) or ord(i) in range(ord('a'),ord('z')+1):
			res=res+i
		else:
			res=res+'_'
	return res


	
def index_show_results(request,v_id=None,d_audio=None):
	f=search_submit_form()
	aname=""
	vname=""
	kw=""
	error_msg=""
	res_list=[]
	res=[]
	particular=0
	if 'results' in request.session.keys():
		res_list=request.session['results']

	
	paginator = Paginator(res_list, 8) # Show 16 contacts per page

	page =request.GET.get('page')
	
	try:
		res = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		res = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		res = paginator.page(paginator.num_pages)
	
	if str(v_id) is not 'all' and int(d_audio) is not 8 :

		if 'tempd' in request.session.keys():
			tempd=request.session['tempd']
			
			dload(str(v_id),int(d_audio),tempd)
			particular=1

			aname='logical/d_audios/{s}.mp3'.format(s=uconvert(tempd[v_id]))
			vname='logical/d_videos/{s}.mp4'.format(s=uconvert(tempd[v_id]))


	context={
	"form":f,
	"error_msg":error_msg,
	"kw":kw,
	"res":res,
	"particular":particular,
	"aname":aname,
	"vname":vname,
	"daudio":int(d_audio)
	}

	return render(request, 'logical/index.html',context)

