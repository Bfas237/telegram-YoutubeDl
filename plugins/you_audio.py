import subprocess
import math
import requests
import os, io, re, sys
import json
import threading
import time
from config import Config
import config
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

from translation import Translation
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
    youtube_dl_url = text
    dldir = Config.DOWNLOAD_LOCATION + "/" + text 
    FORMAT_SELECTION = "Downloading the song in mp3 format <a href='{}'>With the best Quality</a>"
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
    thumbnail = "https://placehold.it/50x50"
    if "thumbnail" in response_json:
        thumbnail = response_json["thumbnail"]
        thumbnail_image = "https://placehold.it/50x50"
    if "thumbnail" in response_json:
        response_json["thumbnail"]
    thumb_image_path = DownLoadFile(thumbnail_image, Config.DOWNLOAD_LOCATION + "/" + ytitle + ".jpg")
    client.edit_message_caption(message.chat.id, sent_id,caption=FORMAT_SELECTION.format(thumbnail), parse_mode='HTML')
    try:
        youtube_dl_format = "0"
        youtube_dl_ext = "mp3"
        thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + ytitle + ".jpg"
        client.edit_message_caption(message.chat.id,sent,caption='{}\nCompleted in {} Seconds'.format(nome,str(int(t2-t1))))
        sentid = client.send_message(chat_id=chat_id, text='Downloading Your video in mp3...', parse_mode='Markdown', reply_to_message_id=msg_id).message_id
        message.delete(sentid)
        description = " " + " \r\n© @Bfas237Bots"
        download_directory = " "
        download_directory = Config.DOWNLOAD_LOCATION + "/" + ytitle + "_" + youtube_dl_format + "." + youtube_dl_ext + ""
        command_to_exec = ["youtube-dl", "--extract-audio", "--audio-format", youtube_dl_ext,"--audio-quality", youtube_dl_format, youtube_dl_url, "-o", download_directory]
        client.send_chat_action(message.chat.id,'UPLOAD_AUDIO')
        sent = client.send_audio(message.chat.id, audio=download_directory, caption=description, title=ytitle, thumb=thumb_image_path, reply_to_message_id=msg_id).message_id
        t2 = time.time()
        client.edit_message_caption(message.chat.id,sent,caption='{}\nCompleted in {} Seconds'.format(description,str(int(t2-t1))))
        client.delete_messages(message.chat.id, sent_id)
    except Exception as error:
        client.edit_message_caption(message.chat.id, sent_id,'Could not send the mp3 file')
        print(error)
    client.send_chat_action(message.chat.id,'CANCEL')
    os.remove(title)
    
    

def audio(message,client):
    text = message.text[5:]
    chat_id = message.chat.id
    msg_id = message.message_id
    if text == '':
        client.send_message(
            chat_id=chat_id,
            text='Use: /mp3 video link or Video name',
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

    
    
    
    
    
    
    
