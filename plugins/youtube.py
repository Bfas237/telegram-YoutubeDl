import subprocess
import math
import requests
import os, io, re, sys
import json
import requests
import subprocess
import os
import threading
import time
from config import Config
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
import youtube_dl

import pyrogram

ydl = youtube_dl.YoutubeDL({'outtmpl': 'dls/%(title)s.%(ext)s', 'format': '140', 'noplaylist': True})

def exec_thread(target, *args, **kwargs):
	t = threading.Thread(target=target, args=args, kwargs=kwargs)
	t.daemon = True
	t.start()

def pretty_size(size):
    units = ['B', 'KB', 'MB', 'GB']
    unit = 0
    while size >= 1024:
        size /= 1024
        unit += 1
    return '%0.2f %s' % (size, units[unit])
def show_progress_bar(stream, chunk, file_handle, bytes_remaining):
         return
def search_ytdd(query):
    url_base = "https://www.youtube.com/results"
    url_yt = "https://www.youtube.com"
    r = requests.get(url_base, params=dict(search_query=query))
    page = r.text
    soup = BeautifulSoup(page, "html.parser")
    id_url = None
    list_videos = []
    for link in soup.find_all('a'):
        url = link.get('href')
        title = link.get('title')
        if url.startswith("/watch") and (id_url != url) and (title is not None):
            id_url = url
            dic = {'title': title, 'url': url_yt + url}
            list_videos.append(dic)
        else:
            pass
    return list_videos

def download(message, client, sent_id, text, msg_id,nome):
	t1 = time.time()
	res = subprocess.getstatusoutput("""cd dls 
youtube-dl '{}'""".format(text))[1]
	re = []
	for	i in res.split('\n'):
		re.append(i)
	for i in re:
		if '[download] ' in i:
			if '.mp4' in i or '.webm' in i:
				title = i
	title = title.replace('[download] ','')
	if ' has already been downloaded' in title:
		title = title.replace(' has already been downloaded','')
	if 'Destination: ' in title:
		title = title.replace('Destination: ','')
	print(title)
	a = re[0]
	print(a)
	number = '-'+a.replace('[youtube] ','').replace(': Downloading webpage','')
	client.edit_message_caption(message.chat.id, sent_id,'Enviando {}'.format(nome))
	try:
		client.send_chat_action(message.chat.id,'UPLOAD_VIDEO')
		sent = client.send_document(message.chat.id,'dls/'+title,caption=nome,reply_to_message_id=msg_id).message_id
		t2 = time.time()
		client.edit_message_caption(message.chat.id,sent,caption='{}\nDemorou {} segundos\n© Made with ❤️ by @Bfas237Bots'.format(nome,str(int(t2-t1))))
		client.delete_messages(message.chat.id, sent_id)
	except Exception as error:
		client.edit_message_caption(message.chat.id, sent_id,'não foi possiviel enviar')
		print(error)
	client.send_chat_action(message.chat.id,'CANCEL')
	os.remove('dls/'+title)
	
def cytdlv(message,client):
    text = message.text[4:]
    chat_id = message.chat.id
    msg_id = message.message_id
    if text == '':
        client.send_message(
            chat_id=chat_id,
            text='**Usage:** `!vid vídeo URL or name`',
            reply_to_message_id=msg_id
        )
    elif 'youtu.be' in text or 'youtube.com' in text:
        sent_id = client.send_message(
            chat_id=chat_id,
            text='⏳ **Obtaining Video Information From Youtube...**',
            parse_mode='Markdown',
            reply_to_message_id=msg_id
        ).message_id
        a = ydl.extract_info('ytsearch:' + text, download=False)['entries'][0]
        time.sleep(3)
    else:
        sent_id = client.send_message(
            chat_id=chat_id,
            text='🔍 **Searching the video on Online...**',
            parse_mode='Markdown',
            reply_to_message_id=msg_id
        ).message_id
        a = ydl.extract_info(text, download=False)
        time.sleep(3)
    for f in a['formats']:
        if f['format_id'] == '140':
            fsize = f['filesize']
            name = a['title']
            text = a['url']
            title = a['title']
            thumb = text.split('v=')
        client.delete_messages(message.chat.id, sent_id)
        print('https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(thumb))
    try:
        sent_id = client.send_photo(message.chat.id,'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(thumb) ,caption='**Downloading:** `{}`'.format(title)).message_id
    except Exception as e:
        sent_id = client.send_photo(message.chat.id,'yt.png' ,caption='An error Occured\n\n' + str(e)).message_id
    nome = title
    time.sleep(2)
    exec_thread(download,message,client,sent_id,text,msg_id,nome)



def search_query_yt(query):
    url_base = "https://www.youtube.com/results"
    url_yt = "https://www.youtube.com"
    r = requests.get(url_base, params=dict(search_query=query))
    page = r.text
    soup = BeautifulSoup(page, "html.parser")
    id_url = None
    list_videos = []
    for link in soup.find_all('a'):
        url = link.get('href')
        title = link.get('title')
        if url.startswith("/watch") and (id_url != url) and (title is not None):
            id_url = url
            dic = {'title': title, 'url': url_yt + url}
            list_videos.append(dic)
        else:
            pass

    dic = {'bot_api_yt':list_videos}
    return dic

def ytdlv(message,client):
	text = message.text[5:]
	chat_id = message.chat.id
	msg_id = message.message_id
	if text == '':
		client.send_message(
			chat_id=chat_id,
			text='Uso: /vid URL do vídeo ou nome',
			reply_to_message_id=msg_id
		)
	elif 'youtu.be' in text or 'youtube.com' in text:
		sent_id = client.send_message(
			chat_id=chat_id,
			text='Obtendo informações do vídeo...',
			parse_mode='Markdown',
			reply_to_message_id=msg_id
		).message_id
		a = search_query_yt(text)
		title = a['bot_api_yt'][0]['title']
		thumb = a['bot_api_yt'][0]['url'].split('v=')[1]
	else:
		sent_id = client.send_message(
			chat_id=chat_id,
			text='Pesquisando o vídeo no YouTube...',
			parse_mode='Markdown',
			reply_to_message_id=msg_id
		).message_id
		a = search_query_yt(text)
		text = a['bot_api_yt'][0]['url']
		title = a['bot_api_yt'][0]['title']
		thumb = text.split('v=')[1]
	client.delete_messages(message.chat.id, sent_id)
	print('https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(thumb))
	try:
		sent_id = client.send_photo(message.chat.id,'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(thumb) ,caption='baixando: {}'.format(title)).message_id
	except:
		sent_id = client.send_photo(message.chat.id,'yt.png' ,caption='baixando: {}'.format(title)).message_id
	nome = title
	from pytube import YouTube 
	SAVE_PATH = "tmp/"
	try: 
		yt = YouTube(text) 
	except Exception as e:
        	client.send_photo(message.chat.id,'yt.png' ,caption='An error Occured\n\n' + str(e))
		print("Connection Error") 
		yt.streams.filter(progressive=True).all()
		yt.register_on_progress_callback(show_progress_bar)
		fn = yt.streams.first()
		try: 
			print(fn)
			fn.download(SAVE_PATH)
		except Exception as e:
        		client.send_photo(message.chat.id,'yt.png' ,caption='An error Occuredsss0\n\n' + str(e))

	client.edit_message_caption(message.chat.id, sent_id,'Enviando {}'.format(title))
	try:
		client.send_chat_action(message.chat.id,'UPLOAD_VIDEO')
		sent = client.send_document(message.chat.id, SAVE_PATH, caption=title,reply_to_message_id=msg_id).message_id
		t2 = time.time()
		client.edit_message_caption(message.chat.id,sent,caption='{}\n\n© Made with ❤️ by @Bfas237Bots'.format(title))
		client.delete_messages(message.chat.id, sent_id)
	except Exception as error:
		client.edit_message_caption(message.chat.id, sent_id,'não foi possiviel enviar')
		print(error)
		client.send_chat_action(message.chat.id,'CANCEL')
		
		
		
