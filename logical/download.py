from __future__ import unicode_literals
import youtube_dl


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
    ydl_opts={ 'outtmpl': 'static/logical/d_videos/{s}.mp4'.format(s=uconvert(tempd[v_id]))}
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
            'outtmpl': 'static/logical/d_audios/{s}.mp3'.format(s=uconvert(tempd[v_id])) 
        }

    try:

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v={i}'.format(i=v_id)])
    except:
        print("Having some bugs...will be fixed soon")


