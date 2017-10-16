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




def dload(v_id,d_audio):
    ydl_opts={}
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
            # 'outtmpl': 'static/{s}.mp3'.format(s=v_id) 
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v={i}'.format(i=v_id)])


