from __future__ import unicode_literals
import youtube_dl
import os
from .models import TemporaryDetails


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')



def uconvert(title):
    res=""
    for i in title:
        if ord(i) in range(ord('A'),ord('Z')+1) or ord(i) in range(ord('a'),ord('z')+1):
            res=res+i
        else:
            res=res+'_'
    return res


def dload(v_id,d_audio,tempd):
    url='https://www.youtube.com/watch?v={i}'.format(i=v_id)


 

    if tempd:
        title=uconvert(tempd[v_id])
    else:
        ydl_opts={}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        if info:
            title=info.get('title',"")
            if title=="":
                title=str(v_id)
            else:
                title=uconvert(title)
        else:
            title=str(v_id)

    obj=TemporaryDetails()
    obj.title=title
    obj.v_id=str(v_id)
    obj.d_audio=int(d_audio)
    obj.save()

    ydl_opts={ 'outtmpl': 'static/logical/d_videos/{s}.mp4'.format(s=title)}


    if d_audio:

  

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320K',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook], 
            'outtmpl': 'static/logical/d_audios/{s}.mp3'.format(s=title) 
        }




    try:


        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
    except:
        print("Having some bugs...will be fixed soon")

    return title





'''
if u make changes in the area that comes under the section 
of celery then u have to restart celery for those changes to get reflected


like in download.py if u make some change then restart celery for those changes to come into action
'''



# if not tempd and not d_audio:
#     if info:
#         title=info.get('title',"")
#     print(title)        
#     if title=="":
#         title=str(v_id)
#     else:
#         title=uconvert(title)
#         if os.path.isfile('static/logical/d_videos/{s}.mp4'.format(s=str(v_id))):
#             os.rename('static/logical/d_videos/{s}.mp4'.format(s=str(v_id)),'static/logical/d_videos/{s}.mp4'.format(s=str(title)))

#         if os.path.isfile('static/logical/d_audios/{s}.mp3'.format(s=str(v_id))):
#             os.rename('static/logical/d_audios/{s}.mp3'.format(s=str(v_id)),'static/logical/d_audios/{s}.mp3'.format(s=str(title)))







# def dload(v_id,d_audio,tempd):
#     ydl_opts={ 'outtmpl': 'static/logical/d_videos/{s}.mp4'.format(s=uconvert(tempd[v_id]))}
#     if d_audio:

#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '320K',
#             }],
#             'logger': MyLogger(),
#             'progress_hooks': [my_hook], 
#             'outtmpl': 'static/logical/d_audios/{s}.mp3'.format(s=uconvert(tempd[v_id])) 
#         }

#     try:

#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             ydl.download(['https://www.youtube.com/watch?v={i}'.format(i=v_id)])
#     except:
#         print("Having some bugs...will be fixed soon")


