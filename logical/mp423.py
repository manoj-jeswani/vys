import moviepy.editor as mp
# .subclip(0,20)



clip = mp.VideoFileClip("myvideo.mp4")
clip.audio.write_audiofile("theaudio.mp3")