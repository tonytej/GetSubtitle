#! /usr/bin/env python

import struct, os, xmlrpclib, gzip, io


url = 'http://api.opensubtitles.org/xml-rpc'

def get_hash(path):
    try:       
        path = path.replace('\\', '')
        longlongformat = '<q'  # little-endian long long
        bytesize = struct.calcsize(longlongformat) 
        f = open(path, "rb") 
        filesize = os.path.getsize(path) 
        hash = filesize 
        if filesize < 65536 * 2: 
            return "SizeError" 
        for x in range(65536/bytesize): 
            buffer = f.read(bytesize) 
            (l_value,)= struct.unpack(longlongformat, buffer)  
            hash += l_value 
            hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number  
        f.seek(max(0,filesize-65536),0) 
        for x in range(65536/bytesize): 
            buffer = f.read(bytesize) 
            (l_value,)= struct.unpack(longlongformat, buffer)  
            hash += l_value 
            hash = hash & 0xFFFFFFFFFFFFFFFF 
        f.close() 
        returnedhash =  "%016x" % hash 
        return returnedhash
    except(IOError): 
            return "IOError"
    
def get_sub(path):
    server = xmlrpclib.Server(url)
    token = server.LogIn('', '', 'en', 'PyGetSubtitle')['token']
    hash = get_hash(path)
    query = {
        'moviehash': hash,
        'sublanguageid': 'eng'
    }
    search = server.SearchSubtitles(token, [query])
    sub_id = search['data'][0]['IDSubtitleFile']
    resp = server.DownloadSubtitles(token, [sub_id])
    data = resp['data'][0]['data']
    decoded = data.decode('base64')
    decompressed = gzip.GzipFile(fileobj=io.BytesIO(decoded)).read()
    path = path.replace('\\', '')
    file = os.path.split(path)[1]
    f_name, f_ext = os.path.splitext(file)
    thedir = os.path.dirname(path)
    with open('{}/{}.srt'.format(thedir, f_name), 'wb') as subtitle:
        subtitle.write(decompressed)
    print resp['status']

while True:
	path = raw_input('Drag the file here... ')[:-1]
	get_sub(path)
    
    
    

