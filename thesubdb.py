#!/usr/bin/env python

import os
import hashlib
import click
import requests

user_agent = {'User-Agent': "SubDB/1.0 (GetSubtitle/0.1; http://github.com/tonytej/GetSubtitle)"}

path = '/Users/Tony/Downloads/True.Detective.S02E02.HDTV.x264-ASAP.mp4'

def get_hash(path):
	"""The API uses an unique hash, calculated from the video 
	file to match a subtitle, implemented on this function"""
        readsize = 64 * 1024
        with open(path, 'rb') as f:
            size = os.path.getsize(path)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()


@click.command()
@click.argument('path')
def getsub(path):
	file = os.path.split(path)[1]
	f_name, f_ext = os.path.splitext(file)
	hash = get_hash(path)
	print hash
	url = 'http://api.thesubdb.com/?action=download&hash={}&language=en'.format(hash)
	r = requests.get(url, headers=user_agent)
	if r.status_code == '404':
		return 'Not Found'
	elif r.status_code == '400':
		return 'Bad Request'
	thedir = os.path.dirname(path)
	with open('{}/{}.srt'.format(thedir, f_name), 'wb') as subtitle:
		subtitle.write(r.content)

if __name__ == '__main__':
    getsub()
