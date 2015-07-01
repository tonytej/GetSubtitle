#Download the english subtitle of a video from thesubdb.com

import requests
import os
import hashlib

user_agent = {'User-Agent': "SubDB/1.0 (GetSubtitle/0.1; http://github.com/tonytej/GetSubtitle)"}

name = "True.Detective.S02E02.HDTV.x264-ASAP.mp4"
def get_hash(name):
	"""The API uses an unique hash, calculated from the video 
	file to match a subtitle"""
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            size = os.path.getsize(name)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

hash = get_hash(name)

url = 'http://sandbox.thesubdb.com/?action=download&hash={}&language=en'.format(hash)

r = requests.get(url, headers=user_agent)