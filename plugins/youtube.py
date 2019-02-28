import requests
import subprocess
import os
import threading
import time
from config import Config
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs


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

def search_yt(query):
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
	res = subprocess.getstatusoutput("""youtube-dl -f best '{}'""".format(text))[1]
	re = []
	for i in res.split('\n'):
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
    exceptt Exception as e:
        sent_id = client.send_photo(message.chat.id,'yt.png' ,caption='An error Occured\n\n' + str(e)).message_id
    nome = title
    time.sleep(2)
    exec_thread(download,message,client,sent_id,text,msg_id,nome)


