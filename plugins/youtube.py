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
import unidecode as ud
import pyrogram

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
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

def DetectFileSize(url):
    r = requests.get(url, allow_redirects=True, stream=True)
    total_size = int(r.headers.get("content-length", 0))
    return total_size



def progress_for_pyrogram(client, current, total, ud_type, message_id, chat_id):
    """if round(current / total * 100, 0) % 10 == 0:
        try:
            client.edit_message_text(
                chat_id,
                message_id,
                text="{}: {} of {}".format(
                    ud_type,
                    humanbytes(current),
                    humanbytes(total)
                )
            )
        except:
            pass"""
    # logger.info("{}: {} of {}".format(ud_type, humanbytes(current), humanbytes(total)))
    pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(math.floor(size)) + " " + Dic_powerN[n] + 'B'
def DownLoadFile(url, file_name, chunk_size, client, ud_type, message_id, chat_id):
    if os.path.exists(file_name):
        os.remove(file_name)
    r = requests.get(url, allow_redirects=True, stream=True)
    # https://stackoverflow.com/a/47342052/4723940
    total_size = int(r.headers.get("content-length", 0))
    downloaded_size = 0
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
                downloaded_size += chunk_size
            if client is not None:
                if ((total_size // downloaded_size) % 5) == 0:
                    time.sleep(0.3)
                    try:
                        client.edit_message_text(
                            chat_id,
                            message_id,
                            text="{}: {} of {}".format(
                                ud_type,
                                humanbytes(downloaded_size),
                                humanbytes(total_size)
                            )
                        )
                    except:
                        pass
    return file_name
from pytube import YouTube 
SAVE_PATH = "tmp/"

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

def prog(client, current, total, message_id, chat_id, required_file_name):
 if round(current/total*100, 0) % 5 == 0:
  try:
   file_size = os.stat(required_file_name).st_size
   client.send_chat_action(chat_id,'UPLOAD_DOCUMENT')
   client.edit_message_caption(chat_id, message_id, "**⬇️ Uploading:** {}% of {}".format(round(current/total*100, 0), str(pretty_size(file_size)))
   )
 
  except:
   pass
def ytdlv(message,client):
    text = message.text[5:]
    chat_id = message.chat.id
    msg_id = message.message_id
    width = 0
    height = 0
    duration = 0
    if len(text) < 1:
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
        text = text
        title = YouTube(text).title
        thumb = text.split('v=')[1]
        thumbnail_image = 'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(thumb)
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
        thumbnail_image = 'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(thumb)
    try:
        file_name = ud.unidecode(YouTube(text).title.replace(" ", "_").replace(".", "-").replace("|", "_").replace("?", "-"))
        file_name = file_name.strip()
        download_directory = ud.unidecode(SAVE_PATH + '{}.mp4'.format(file_name))
        sent_id = client.send_photo(message.chat.id,'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(thumb) ,caption='Downloading: {}'.format(title)).message_id
        yt = YouTube(text).streams.filter(subtype='mp4', progressive=True).first()

        print("Downloading..." + YouTube(text).title)
        yt.download(SAVE_PATH, filename=file_name)
        thumb_image_path = DownLoadFile(
                thumbnail_image,
                SAVE_PATH + str(message.from_user.id) + ".jpg",
                8192,
                None,  # bot,
                "Downloading:",
                sent_id,
                message.chat.id
            )

        print(thumbnail_image)
        metadata = extractMetadata(createParser(download_directory))
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if os.path.exists(thumb_image_path):
            width = 0
            height = 0
            metadata = extractMetadata(createParser(thumb_image_path))
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
                # resize image
                # ref: https://t.me/PyrogramChat/44663
                # https://stackoverflow.com/a/21669827/4723940
            Image.open(thumb_image_path).convert(
                    "RGB").save(thumb_image_path)
            img = Image.open(thumb_image_path)
                # https://stackoverflow.com/a/37631799/4723940
            img.thumbnail((90, 90))
            img.save(thumb_image_path, "JPEG")
                # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
        else:
            thumb_image_path = None
        client.edit_message_caption(message.chat.id, sent_id,'Uploading... {}'.format(title))
        final = SAVE_PATH + '{}.mp4'.format(file_name)
        client.send_chat_action(message.chat.id,'UPLOAD_VIDEO')
        sent = client.send_video(message.chat.id, video=final, caption=title,duration=duration,width=width,height=height,supports_streaming=True,thumb=thumb_image_path,reply_to_message_id=msg_id, progress = prog, progress_args = (sent_id, message.chat.id, final)).message_id
        t2 = time.time()
        client.edit_message_caption(message.chat.id,sent,caption='{}\n\n© Made with ❤️ by @Bfas237Bots'.format(title))
        client.delete_messages(message.chat.id, sent_id)

    except Exception as e:
        sent_id = client.send_photo(message.chat.id,'yt.png' ,caption='An error Occured\n\n' + str(e)).message_id
        print(str(e))
        client.send_chat_action(message.chat.id,'CANCEL')
    try:
        os.remove(download_directory)
        os.remove(thumb_image_path)
    except:
        pass
