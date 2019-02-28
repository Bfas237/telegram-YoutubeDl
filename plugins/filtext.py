from pyrogram import Client, Filters
import config
import time
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
    from urllib.parse import quote_plus
    import urllib.request
    python3 = True
except ImportError:
    from urllib import quote_plus
    import urllib2
    python3 = False

def progress_callback_simple(downloaded,total):
    sys.stdout.write(
        "\r" +
        (len(str(total))-len(str(downloaded)))*" " + str(downloaded) + "/%d"%total +
        " [%3.2f%%]"%(100.0*float(downloaded)/float(total))
    )
    sys.stdout.flush()

def filedownload(srcurl, dstfilepath, progress_callback=None, block_size=8192):
    def _download_helper(response, out_file, file_size):
        if progress_callback!=None: progress_callback(0,file_size)
        if block_size == None:
            buffer = response.read()
            out_file.write(buffer)

            if progress_callback!=None: progress_callback(file_size,file_size)
        else:
            file_size_dl = 0
            while True:
                buffer = response.read(block_size)
                if not buffer: break

                file_size_dl += len(buffer)
                out_file.write(buffer)
                out_file.flush()

                if progress_callback!=None: progress_callback(file_size_dl,file_size)
    with open(dstfilepath,"wb") as out_file:
        if python3:
            with urllib.request.urlopen(srcurl) as response:
                file_size = int(response.getheader("Content-Length"))
                _download_helper(response,out_file,file_size)
                return dstfilepath
        else:
            response = urllib2.urlopen(srcurl)
            meta = response.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            _download_helper(response,out_file,file_size)
            return dstfilepath

import traceback

from bs4 import BeautifulSoup
from shutil import copyfile
ydl = youtube_dl.YoutubeDL({'outtmpl': 'dls/%(title)s.%(ext)s', 'format': '140', 'noplaylist': True})
app = config.app
user_id = config.user_id
prefix = config.prefix

if config.language == "english":
    from languages.english import fetching_download_link, download_job_started, download_successfull, upload_job_started
def exec_thread(target, *args, **kwargs):
  t = threading.Thread(target=target, args=args, kwargs=kwargs)
  t.daemon = True
  t.start()

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')





@app.on_message(Filters.text)
def move(client, message):
  if message.text.startswith('/mp3') or message.text.startswith('!mp3'):
      exec_thread(audio.audio,message,client)
  if message.text.startswith('/vid') or message.text.startswith('!vid'):
      exec_thread(youtube.ytdlv,message,client)
