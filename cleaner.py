import os
# from datetime import datetime
# from threading import Timer




# x=datetime.today()
# y=x.replace(day=x.day+1, hour=3, minute=0, second=0, microsecond=0)
# delta_t=y-x

# secs=delta_t.seconds+1


def clean_fun():

	os.system("cd ~/vys/static/logical && rm -r d_audios")
	os.system("cd ~/vys/static/logical && mkdir d_audios")
	os.system("cd ~/vys/static/logical && rm -r d_videos")
	os.system("cd ~/vys/static/logical && mkdir d_videos")

# t = Timer(secs, clean_fun)
# t.start()

clean_fun()