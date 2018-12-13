from pyrogram import Client, Filters
import config
import time
import urbandict as ud
import sys, os, re, sys
import warnings, random
from random import randint
import requests
import threading
import io
import urllib
import subprocess
import plugins.you_audio as audio
import plugins.youtube as youtube
import youtube_dl

from contextlib import redirect_stdout
try:
    from urllib import quote_plus  # Python 2.X
except ImportError:
    from urllib.parse import quote_plus  # Python 3+

from bs4 import BeautifulSoup
from pyaxmlparser import APK
from shutil import copyfile
ydl = youtube_dl.YoutubeDL({'outtmpl': 'dls/%(title)s.%(ext)s', 'format': '140', 'noplaylist': True})
app = config.app
user_id = config.user_id
prefix = config.prefix

if config.language == "english":
    from languages.english import fetching_download_link, download_job_started, download_successfull, upload_job_started, no_result_found  
def exec_thread(target, *args, **kwargs):
	t = threading.Thread(target=target, args=args, kwargs=kwargs)
	t.daemon = True
	t.start()

from hurry.filesize import size, alternative
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


def shuffle(word):
    wordlen = len(word)
    word = list(word)
    for i in range(0,wordlen-1):
        pos = randint(i+1,wordlen-1)
        word[i], word[pos] = word[pos], word[i]
    word = "".join(word)
    return word

def pretty_size(sizes):
    units = ['B', 'KB', 'MB', 'GB']
    unit = 0
    while sizes >= 1024:
        sizes /= 1024
        unit += 1
    return '%0.2f %s' % (sizes, units[unit])
def dosomething(buf):
    """Do something with the content of a file"""
    sleep(0.01)
    pass

    
    
        
def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]




@app.on_message(Filters.text & Filters.chat("bfas237off"))
def move(client, message):
  if message.text.startswith('/ymp3') or message.text.startswith('!ytdl'):
      exec_thread(audio.ytdlv,message,client)
  if message.text.startswith('/ytdl') or message.text.startswith('!ytdl'):
      exec_thread(youtube.ytdlv,message,client)
  if message.text.startswith('/dl') or message.text.startswith('!dl'):
      first_time = time.time()
      word = message.text[4:]
      search = " ".join(word)
      sent = client.send_message(message.chat.id, fetching_download_link.format(search), reply_to_message_id=message.message_id).message_id 
      ress = requests.get('https://apkpure.com/search?q={}&region='.format(quote_plus(search)), headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5'
    }).text 
      APPS = []
      soups = BeautifulSoup(ress, "html.parser")
      for i in soups.find('div', {'id': 'search-res'}).findAll('dl', {'class': 'search-dl'}):
      	app = i.find('p', {'class': 'search-title'}).find('a')
      	app_url = 'https://apkpure.com' + app['href']
      	APPS.append((app.text,
                     i.findAll('p')[1].find('a').text,
                     'https://apkpure.com' + app['href']))
      rnd = "123456789abcdefgh-_"
      servers = shuffle(rnd)
      time.sleep(10)
			
      if len(APPS) > 0:
        client.edit_message_text(message.chat.id, sent, download_job_started.format(servers, APPS[00][2]))
      link = APPS[00][2]
      time.sleep(5)
      res = requests.get(link + '/download?from=details', headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5'
    }).text
      soup = BeautifulSoup(res, "html.parser").find('a', {'id': 'download_link'})
      if soup['href']:
        r = requests.get(soup['href'], stream=True, allow_redirects=True, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5'})
        required_file_name = get_filename_from_cd(r.headers.get('content-disposition'))
        with open(required_file_name, 'wb') as apk:
          for chunk in r.iter_content(chunk_size=1024):
            total_length = r.headers.get('content-length')
            dl = 0
            total_length = int(total_length)
            if chunk:
                dl += len(chunk)
                done = int(100 * dl / total_length)
                apk.write(chunk)
                apk.flush()
      second_time = time.time()
      client.edit_message_text(message.chat.id, sent, download_successfull.format(str(second_time - first_time)[:5]))
      time.sleep(5)
      client.edit_message_text(message.chat.id, sent, upload_job_started)
      client.delete_messages(message.chat.id, sent)
      client.delete_messages(message.chat.id, message.message_id)
      t1 = time.time()
      client.send_chat_action(message.chat.id,'UPLOAD_DOCUMENT')
      sentq = client.send_document(message.chat.id, required_file_name, caption="File Upload Sucessfull", reply_to_message_id=message.message_id).message_id
      time.sleep(5)
      t2 = time.time()
      client.edit_message_caption(message.chat.id,sentq,caption='{}\n\n**File Size**: {}\n\nPowered By **Bfas237 Projects**'.format(required_file_name, str(pretty_size(total_length))))
      os.remove(required_file_name)
      
          
@app.on_message(Filters.text & Filters.chat("Bfas237group"))
def move(client, message):
  if "Oft" in message.text:
      client.send_message("bfas237off", "[{}](tg://user?id={}) **wrote:**\n{}\n\n**⬇️ ᴘʟᴇᴀsᴇ ᴄᴏɴᴛɪɴᴜᴇ ʜᴇʀᴇ ⬇️**".format(message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id, message.reply_to_message.text))
      message.reply("I moved this discussion to the [Offtopic Group ↗️](https://t.me/bfas237off/{})".format(message.reply_to_message.message_id, message.reply_to_message.text), reply_to_message_id=message.reply_to_message.message_id, quote=True)
      client.delete_messages(
    "Bfas237group",
    message_ids=message.message_id
)
      client.delete_messages(
    "bfas237off",
    message_ids=message.reply_to_message.message_id
)
@app.on_message(Filters.text & Filters.chat("bfas237off"))
def move(client, message):
    if "Ont" in message.text:
        client.send_message("Bfas237group", "[{}](tg://user?id={}) **wrote:**\n{}\n\n**⬇️ ᴘʟᴇᴀsᴇ ᴄᴏɴᴛɪɴᴜᴇ ʜᴇʀᴇ ⬇️**".format(message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id, message.reply_to_message.text))
        message.reply("The Main group has been created for this discussion so why not join [Offtopic Group ↗️](https://t.me/bfas237off/{})".format(message.reply_to_message.message_id, message.reply_to_message.text), reply_to_message_id=message.reply_to_message.message_id, quote=True)
        client.delete_messages(
    "bfas237off",
    message_ids=message.message_id
)
        client.delete_messages(
    "Bfas237group",
    message_ids=message.reply_to_message.message_id
)
