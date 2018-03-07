from django.shortcuts import render
from .forms import *
from .search import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect
from .download import *
from urllib.parse import urlparse, parse_qs
import moviepy.editor as mp
import re
from .utils import code_generator,create_shortcode
import os
from django.conf import settings
PATH=settings.STATIC_ROOT
import json
from logical.tasks import load_item,load_search
from celery import uuid
from celery.result import AsyncResult
from .models import TemporaryDetails,Search_Result
from collections import OrderedDict

from django.views.decorators.csrf import csrf_exempt
def index_view(request):
	context={}
	return render(request, 'logical/index.html',context)




# Create your views here.
def mp3_get_query(request):
	kw=""
	error_msg=""
	task_id=""
	if request.is_ajax() and request.method=='POST':

		resp={}
		f=search_submit_form(request.POST)
		if f.is_valid():
			kw=f.cleaned_data.get('keyword')
		if kw=="":
			error_msg=f.errors.get('keyword')
			f.errors['keyword']=""
			resp['data']=False
		else:
		
			task_id = uuid()
			ret=load_search.apply_async((str(kw),),task_id=task_id,queue='vys')
			resp['data']=True
		resp['kw']=kw
		resp['tid']=task_id
		resp['emsg']=error_msg
		return HttpResponse(json.dumps(resp), content_type ='application/json; charset=utf8')

	else:
		f=search_submit_form()
	context={
		"form":f,
		"error_msg":error_msg,
		}

	return render(request, 'logical/sdownload.html',context)


@csrf_exempt
def log_search_result_view(request):
	skey=""
	if request.is_ajax() and 'skey' in request.POST.keys():
		skey=request.POST['skey']
		obj=Search_Result.objects.filter(kw=str(skey)).first()
		res_list=obj.sres
		request.session['results']=res_list
		tempd={}
		tempd['all']="_"
		for i in res_list:
			tempd[i['v_id']]=i['title']

		request.session['tempd']=tempd
		

		#obj.delete()
		data=True

	else:
		# 'This is not an ajax request or invalid data'
		data=False
	
	return HttpResponse(json.dumps(data), content_type ='application/json; charset=utf8')





def mp3_show_results(request):

	res_list=[]
	res=[]
	
	if 'results' in request.session.keys():
		res_list=request.session['results']
	
	paginator = Paginator(res_list, 8) 

	page =request.GET.get('page')

	try:
		res = paginator.page(page)

	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		res = paginator.page(paginator.num_pages)
	except:
		# If page is not an integer, deliver first page.
		res = paginator.page(1)


	context={
		"res":res,
	}

	return render(request, 'logical/show_res.html',context)




def uconvert(title):
	res=""
	for i in title:
		if ord(i) in range(ord('A'),ord('Z')+1) or ord(i) in range(ord('a'),ord('z')+1):
			res=res+i
		else:
			res=res+'_'
	return res


@csrf_exempt
def get_file_link(request):
	if request.is_ajax() and'v_id' and 'd_audio' and 'iyview' in request.POST.keys():
		v_id=request.POST['v_id']
		d_audio=request.POST['d_audio']
		iyview=request.POST['iyview']
		
		if str(v_id) is not 'all' and int(d_audio)  in (0,1) and int(iyview)  in (0,1) :
			mm=""
			if int(iyview):
				obj=TemporaryDetails.objects.filter(v_id=str(v_id),d_audio=int(d_audio)).first()
				mm=obj.title
				obj.delete()
			else:

				if 'tempd' in request.session.keys():
					tempd=request.session['tempd']
					mm=uconvert(tempd[v_id])
			
			print('got ' ,v_id)
			print(d_audio)

			vname=""
			aname=""
			if int(d_audio):

				cmd="cd {path}/logical/d_audios; ls {file}.*".format(path=PATH,file=mm)
				mm=os.popen(cmd).read()[:-1]
				aname='logical/d_audios/{s}'.format(s=mm)
				request.session[v_id]={'d_audio':d_audio,'fpath':settings.STATIC_URL+aname}
	
			else:
				cmd="cd {path}/logical/d_videos; ls {file}.*".format(path=PATH,file=mm)
				mm=os.popen(cmd).read()[:-1]
				vname='logical/d_videos/{s}'.format(s=mm)
				request.session[v_id]={'d_audio':d_audio,'fpath':settings.STATIC_URL+vname}

			data={'aname':settings.STATIC_URL+aname,'vname':settings.STATIC_URL+vname}

		else:
			data = 'Post entries not correct'
	else:
		data = 'This is not an ajax request'
	return HttpResponse(json.dumps(data), content_type ='application/json; charset=utf8')






@csrf_exempt
def load_state(request):

	if request.is_ajax():
		if 'task_id' in request.POST.keys() and request.POST['task_id']:
			task_id = request.POST['task_id']
			data = AsyncResult(task_id).successful()
			
			# data = AsyncResult(task_id).successful()


			#data = task.result or task.state


		else:
			data = 'No task_id in the request'
	else:
		data = 'This is not an ajax request'
	return HttpResponse(json.dumps(data), content_type ='application/json; charset=utf8')






def load_view(request,v_id=None,d_audio=None):
	if str(v_id) is not 'all' and int(d_audio) is not 8 :

		if 'tempd' in request.session.keys():
			tempd=request.session['tempd']
			ret=False
			task_id = uuid()
			ret=load_item.apply_async((str(v_id),int(d_audio),tempd),task_id=task_id,queue='vys')
			print(task_id)
			#ret=load_item.delay(str(v_id),int(d_audio),tempd)

	context={'task_id':str(task_id),'v_id':v_id,'d_audio':d_audio,'iyview':0}
	return render(request, 'logical/loading.html',context)






def get_id(url):
    u_pars = urlparse(url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]






				# if int(a):
				# 	cmd="cd {path}logical/d_audios; ls {file}.*".format(path=PATH,file=mm)
				# 	mm=os.popen(cmd).read()[:-1]
				# 	aname='logical/d_audios/{s}'.format(s=mm)
				# else:
				# 	cmd="cd {path}logical/d_videos; ls {file}.*".format(path=PATH,file=mm)
				# 	mm=os.popen(cmd).read()[:-1]
				# 	vname='logical/d_videos/{s}'.format(s=mm)





def yv_view(request,a=None):
	error_msg=""
	lnk=""
	if request.method=='POST':

		f=utube_submit(request.POST)
		if f.is_valid():
			lnk=f.cleaned_data.get('link')
		if lnk=="":
			error_msg=f.errors.get('link')
			f.errors['link']=""
		else:
			vid=get_id(lnk)
			if vid is not None:
				
				mapy={}

				ret=False
				task_id = uuid()
				ret=load_item.apply_async((str(vid),int(a),mapy),task_id=task_id,queue='vys')
				print(task_id)
				context={'task_id':str(task_id),'v_id':str(vid),'d_audio':int(a),'iyview':1}
				return render(request, 'logical/loading.html',context)


	else:
		f=utube_submit()
	
	context={
		"form":f,
		"error_msg":error_msg,

		"ia":int(a)
		}


	return render(request, 'logical/yvdownload.html',context)



def on_play(request,v_id=None):
	is_audio=1
	fpath=""
	name=""
	print(request.session["cnv"])
	if v_id in request.session or v_id=="cnv":
		if v_id=="cnv":
			data=request.session["cnv"]
		else:
			data=request.session[v_id]
		is_audio=int(data['d_audio'])
		fpath=data['fpath']
		name=os.path.basename(fpath)
		#del request.session[v_id]
	context={
		"is_audio":is_audio,
		"fpath":fpath,
		'name':name
		}

	return render(request, 'logical/online_play.html',context)

	

# def yv_view(request,a=None):
# 	lnk=""
# 	particular=0
# 	error_msg=""
# 	vname=""
# 	aname=""
# 	if request.method=='POST':

# 		f=utube_submit(request.POST)
# 		if f.is_valid():
# 			lnk=f.cleaned_data.get('link')
# 		if lnk=="":
# 			error_msg=f.errors.get('link')
# 			f.errors['link']=""
# 		else:
# 			vid=get_id(lnk)
# 			if vid is not None:
# 				mm=""
# 				mapy={}

# 				mm=dload(str(vid),int(a),mapy)
# 				particular=1
# 				if int(a):
# 					cmd="cd {path}logical/d_audios; ls {file}.*".format(path=PATH,file=mm)
# 					mm=os.popen(cmd).read()[:-1]
# 					aname='logical/d_audios/{s}'.format(s=mm)
# 				else:
# 					cmd="cd {path}logical/d_videos; ls {file}.*".format(path=PATH,file=mm)
# 					mm=os.popen(cmd).read()[:-1]
# 					vname='logical/d_videos/{s}'.format(s=mm)




# 	else:
# 		f=utube_submit()
# 	context={
# 		"form":f,
# 		"error_msg":error_msg,
# 		"particular":particular,
# 		"vname":vname,
# 		"aname":aname,
# 		"ia":int(a)
# 		}


# 	return render(request, 'logical/yvdownload.html',context)



def repspace(fname):

	fname=fname.replace(" ","_")
	return str(fname)

def get_extension(name):
	return re.findall(r'.\w+$',name)[0][:]




def cn_view(request):

	if request.method == 'POST':
		got_up=''

		if 'up' in request.FILES:
			got_up=request.FILES['up'].name

		ext=get_extension(str(got_up))
		code=create_shortcode()

		request.FILES['up'].name=str(code+ext)

		form = Uploadmp4Form(request.POST, request.FILES)

		if form.is_valid():
			form=form.save(commit=False)
			form.code=code
			form.save()

			fname=repspace(str(got_up))
			clip = mp.VideoFileClip("media/videouploads/"+str(code+ext))
			lname=fname.replace(ext,str(code+'.mp3'))
			fname="static/logical/d_audios/"+lname
			clip.audio.write_audiofile(fname)
			cmd='cd media/videouploads; rm {s}'.format(s=str(code+ext))
			os.system(cmd)
			instance=Uploadmp4.objects.filter(code=code)
			instance.delete()
			aname='logical/d_audios/'+lname
			context={
				"res":0,
				"particular":1,
				"aname":aname,
				"vname":'',
				"daudio":int(1)
				}
			res={}
			res['data']= " {s} ".format(s=settings.STATIC_URL+aname)
			request.session["cnv"]={'d_audio':1,'fpath':res['data']}
			return HttpResponse(json.dumps(res))
			# return render(request, 'logical/sdownload.html',context)

	else:
		form = Uploadmp4Form()


	context={'form': form}
	return render(request, 'logical/convertmp43.html',context)
