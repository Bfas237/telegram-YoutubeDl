import subprocess
import math
import requests
import os, io, re, sys
import json
import threading
import time
from config import Config
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
import pyrogram
def exec_thread(target, *args, **kwargs):
	t = threading.Thread(target=target, args=args, kwargs=kwargs)
	t.daemon = True
	t.start()
def DownLoadFile(url, file_name):
    if not os.path.exists(file_name):
        r = requests.get(url, allow_redirects=True, stream=True)
        with open(file_name, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=Config.CHUNK_SIZE):
                fd.write(chunk)
    return file_name

    # create download directory, if not exist


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    #2**10 = 1024
    if not size:
      return ""
    power = 2**10
    n = 0
    Dic_powerN = {0 : ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /=  power
        n += 1
    return str(math.floor(size)) + " " + Dic_powerN[n] + 'B'

def search_query_yt(query):
	URL_BASE = "https://www.youtube.com/results?search_query=%s"%(query)
	#URL_BASE = "https://www.youtube.com/results?search_query=oi"
	url_yt= "https://www.youtube.com"
	r = requests.get(URL_BASE)
	page = r.text
	soup = bs(page,"html.parser")
	id_url = None
	list_videos = []
	for link in soup.find_all('a'):
		url = link.get('href')
		title = link.get('title')
		if url.startswith("/watch") and (id_url!=url) and (title!=None):
			id_url = url
			dic = {'title':title,'url':url_yt+url}
			list_videos.append(dic)
		else:
			pass
	dic = {'bot_api_yt':list_videos}
	return dic

def dld(message, client, sent_id, text, msg_id,nome):
	if not os.path.isdir(Config.DOWNLOAD_LOCATION):
		os.makedirs(Config.DOWNLOAD_LOCATION)
	t1 = time.time()
	dldir = Config.DOWNLOAD_LOCATION + "/" + text 
	FORMAT_SELECTION = "Select the desired format: <a href='{}'>file size might be approximate</a>"
	command_to_exec = ["youtube-dl", "--no-warnings", "-j", text]
	t_response = subprocess.check_output(command_to_exec, stderr=subprocess.STDOUT)
	x_reponse = t_response.decode("UTF-8")
	response_json = json.loads(x_reponse)
	ytitle = response_json["title"]
	inline_keyboard = []
	for formats in response_json["formats"]:
		format_id = formats["format_id"]
		format_string = formats["format"]
		format_ext = formats["ext"]
		approx_file_size = ""
		if "filesize" in formats:
			approx_file_size = humanbytes(formats["filesize"])
		
	inline_keyboard.append([
                    pyrogram.InlineKeyboardButton("MP3 " + "(" + "medium" + ")", callback_data="5:mp3".encode("UTF-8"))
                ])
	inline_keyboard.append([
                    pyrogram.InlineKeyboardButton("MP3 " + "(" + "best" + ")", callback_data="0:mp3".encode("UTF-8"))
                ])
	reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)
	thumbnail = "https://placehold.it/50x50"
	if "thumbnail" in response_json:
		thumbnail = response_json["thumbnail"]
		thumbnail_image = "https://placehold.it/50x50"
	if "thumbnail" in response_json:
		response_json["thumbnail"]
	
	thumb_image_path = DownLoadFile(thumbnail_image, Config.DOWNLOAD_LOCATION + "/" + ytitle + ".jpg")
	client.send_message(
                    message.chat.id,
                    text=FORMAT_SELECTION.format(thumbnail),
                    reply_markup=reply_markup,
                    parse_mode=pyrogram.ParseMode.HTML,
                    reply_to_message_id=update.message_id
                )
	try:
		
		client.send_chat_action(message.chat.id,'UPLOAD_VIDEO')
		sent = client.send_document(message.chat.id,title,caption=nome,reply_to_message_id=msg_id).message_id
		t2 = time.time()
		client.edit_message_caption(message.chat.id,sent,caption='{}\nCompleted in {} Seconds'.format(nome,str(int(t2-t1))))
		client.delete_messages(message.chat.id, sent_id)
	except Exception as error:
		client.edit_message_caption(message.chat.id, sent_id,'Could not send the video')
		print(error)
	client.send_chat_action(message.chat.id,'CANCEL')
	os.remove(title)

def audio(message,client):
	text = message.text[6:]
	chat_id = message.chat.id
	msg_id = message.message_id
	if text == '':
		client.send_message(
			chat_id=chat_id,
			text='Uso: /ytdl URL do vídeo ou nome',
			reply_to_message_id=msg_id
		)
	elif 'youtu.be' in text or 'youtube.com' in text:
		sent_id = client.send_message(
			chat_id=chat_id,
			text='Obtaining Video Information...',
			parse_mode='Markdown',
			reply_to_message_id=msg_id
		).message_id
		a = search_query_yt(text)
		title = a['bot_api_yt'][0]['title']
		thumb = a['bot_api_yt'][0]['url'].split('v=')[1]
	else:
		sent_id = client.send_message(
			chat_id=chat_id,
			text='Searching the video on YouTube...',
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
		sent_id = client.send_photo(message.chat.id,'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(thumb) ,caption='Downloading: {}'.format(title)).message_id
	except:
		sent_id = client.send_photo(message.chat.id,'yt.png' ,caption='Downloading: {}'.format(title)).message_id
	nome = title
	exec_thread(dld,message,client,sent_id,text,msg_id,nome)
