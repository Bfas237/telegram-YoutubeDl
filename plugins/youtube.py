import requests
import subprocess
import os
import threading
import time
from config import Config
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def exec_thread(target, *args, **kwargs):
	t = threading.Thread(target=target, args=args, kwargs=kwargs)
	t.daemon = True
	t.start()

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

def download(message, client, sent_id, text, msg_id,nome):
	t1 = time.time()
	res = subprocess.getstatusoutput("""youtube-dl -f best '{}'""".format(text))[1]
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
	client.edit_message_caption(message.chat.id, sent_id,'**Uploading `{}` to telegram in progress**'.format(nome))
	time.sleep(5)
	try:
		client.send_chat_action(message.chat.id,'UPLOAD_VIDEO')
		description = " " + " \r\n© Made with ❤️ by @Bfas237Bots "
		sent = client.send_document(message.chat.id,title,caption=nome,reply_to_message_id=msg_id).message_id
		t2 = time.time()
		time.sleep(5)
		client.edit_message_caption(message.chat.id,sent,caption='{}\n\n**Upload Completed in** `{}` **Seconds**'.format(nome,str(int(t2-t1))))
		time.sleep(3)
		client.edit_message_caption(message.chat.id,sent,caption='**{}**\n\n\n{}\n'.format(nome,description))
		client.delete_messages(message.chat.id, msg_id)
		client.delete_messages(message.chat.id, sent_id)
	except Exception as error:
		client.edit_message_caption(message.chat.id, sent_id,'**Could not send the video file:**')
		print(error)
	client.send_chat_action(message.chat.id,'CANCEL')
	os.remove(title)

def ytdlv(message,client):
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
			text='⏳ **Obtaining Video Information...**',
			parse_mode='Markdown',
			reply_to_message_id=msg_id
		).message_id
		a = search_query_yt(text)
		time.sleep(5)
		title = a['bot_api_yt'][0]['title']
		thumb = a['bot_api_yt'][0]['url'].split('v=')[1]
	else:
		sent_id = client.send_message(
			chat_id=chat_id,
			text='🔍 **Searching the video on YouTube...**',
			parse_mode='Markdown',
			reply_to_message_id=msg_id
		).message_id
		a = search_query_yt(text)
		time.sleep(5)
		text = a['bot_api_yt'][0]['url']
		title = a['bot_api_yt'][0]['title']
		thumb = text.split('v=')[1]
	client.delete_messages(message.chat.id, sent_id)
	print('https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(thumb))
	try:
		sent_id = client.send_photo(message.chat.id,'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(thumb) ,caption='**Downloading:** `{}`'.format(title)).message_id
	except:
		sent_id = client.send_photo(message.chat.id,'yt.png' ,caption='**Downloading:** `{}`'.format(title)).message_id
	nome = title
	time.sleep(5)
	exec_thread(download,message,client,sent_id,text,msg_id,nome)
