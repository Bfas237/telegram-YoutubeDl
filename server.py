import time
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from bs4 import BeautifulSoup
from pyaxmlparser import APK
from shutil import copyfile
import subprocess
import math
import requests
from requests import exceptions
import sys, os, re, sys, io
import warnings, random
from random import randint
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram import Client, Filters, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ForceReply
from contextlib import redirect_stdout
from fake_useragent import UserAgent
ua = UserAgent()

from fake_useragent import FakeUserAgentError

from translation import Translation

APPS = []


active_chats = {
}

# the Telegram trackings
from chatbase import Message

  
  
fetching_download_link = "🔁 Searching for **{}** in progress."
download_job_started = "Search was successful. \n\n ⬇️ **Download Server** [apkpure.com]({}) \n\nI am now downloading the file"
download_successfull = "Download Was was completed in `{}`"
upload_job_started = "Now Uploading to telegram in progres and that should not take long."
no_result_found = "Oops! There was an error!!!"  
  
import os
api_id = 256406
api_hash = "31fd969547209e7c7e23ef97b7a53c37"
class Config(object):
    # get a token from https://chatbase.com
    CHAT_BASE_TOKEN = os.environ.get("CHAT_BASE_TOKEN", "880f05a1-685c-4909-a8f6-b17463625eba")
    # get a token from @BotFather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "773593833:AAEMjP5M7LveexMhVTpjoKOn_X9TDNbTggg")
    # your domain to show when download file is greater than MAX_FILE_SIZE
    HTTP_DOMAIN = os.environ.get("HTTP_DOMAIN", "https://example.com/")
    # for running on Heroku.com
    PORT = int(os.environ.get('PORT', 5000))
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH")
    # Get these values from my.telegram.org
    # Array to store users who are authorized to use the bot
    AUTH_USERS = set(str(x) for x in os.environ.get("AUTH_USERS", "197005208").split())
    # the download location, where the HTTP Server runs
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    # Telegram maximum file upload size
    MAX_FILE_SIZE = 50000000
    TG_MAX_FILE_SIZE = 14000000000
    # chunk size that should be used with requests
    CHUNK_SIZE = 128
    # default thumbnail to be used in the videos
    DEF_THUMB_NAIL_VID_S = "https://placehold.it/90x90"
app = Client(
    "777521418:AAGqM3e9xItYpTE-zINAizVCPyDMGR_UPIo",
    api_id=api_id,
    api_hash=api_hash)

from pyrogram.api.errors import (
    BadRequest, Flood, InternalServerError,
    SeeOther, Unauthorized, UnknownError
)
import sys
try:
    from urllib.parse import quote_plus
    import urllib.request
    python3 = True
except ImportError:
    from urllib import quote_plus
    import urllib2
    python3 = False
import traceback
from pyrogram import Client, Filters

import requests
import threading
import io
import urllib
import subprocess

import traceback
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


def dynamic_data(data):
    return Filters.create(
        name="DynamicData",
        func=lambda filter, callback_query: filter.data == callback_query.data,
        data=data  # "data" kwarg is accessed with "filter.data"
    )
def DownLoadFile(url, file_name):
    if not os.path.exists(file_name):
        r = requests.get(url, allow_redirects=True, stream=True)
        with open(file_name, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=Config.CHUNK_SIZE):
                fd.write(chunk)
    return file_name
def search(query, options={}):
  try:
      ua = UserAgent()
  except FakeUserAgentError:
      pass
  base_headers = {
        'User-Agent':  ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
  headers = dict(base_headers, **options)
  try:
    res = requests.get('https://apkpure.com/search?q={}&region='.format(quote_plus(query)), headers=headers).text
    soup = BeautifulSoup(res, "html.parser")
    for i in soup.find('div', {'id':'search-res'}).findAll('dl', {'class':'search-dl'}):
        app = i.find('p', {'class':'search-title'}).find('a')
        APPS.append((app.text,
                    i.findAll('p')[1].find('a').text,
                    'https://apkpure.com' + app['href']))
  except (ProtocolError, ConnectionError, ConnectionResetError, ReadTimeout, Timeout, TimeoutError, ConnectTimeout) as e:
    bot.send_message(
            chat_id=update.from_user.id,
            text=e,
            reply_to_message_id=update.message_id
        )
    return None
fetching_download_link = "🔁 Searching for **{}** in progress."
download_job_started = "\n ⬇️ **Download Server** [{}]({}) in progress"
download_successfull = "Download Was was completed in `{}`"
upload_job_started = "Now Uploading to telegram in progres and that should not take long."
no_result_found = "Oops! There was an error!!!"
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


import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)


## The telegram Specific Functions
def error(bot, update, error):
    # TRChatBase(update.from_user.id, update.text, "error")
    logger.warning('Update "%s" caused error "%s"', update, error)

def messages(bot, update):
        global active_chats

        user_chat = active_chats.get(update.from_user.id, None)
        if user_chat is None:
            bot.send_message(chat_id=update.from_user.id,
                             text="DEBUG-WARNING: You are not in active_chats.")
            return

        actions = user_chat.get('actions', None)
        if actions is None:
            bot.send_message(chat_id=update.from_user.id,
                             text="DEBUG-WARNING: You have no actions list.")
            return
        if len(actions) == 0:
            bot.send_message(chat_id=update.from_user.id,
                             text="DEBUG: You have empty actions list.")
            return
        
        
        recent_action = actions[-1]
        #bot.send_message(chat_id=update.from_user.id, text="DEBUG: last action: {}".format(recent_action))
        if recent_action == 'apks':
            if len(update.text) < 5:
              
                apk_string = "{}".format("apks")
                bot.send_message(
        chat_id=update.from_user.id,
        text="**📱 Apk Downloader**\n\n__Step 2 of 3__\n\n"
                                      "🔎 **Search Query too short!** Please try again.",
        reply_markup=InlineKeyboardMarkup(
        [
          
            [  
                InlineKeyboardButton("⬅️ Go Back", callback_data=apk_string.encode("UTF-8")),
            ]
        ]
    ),
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True)
              
                return
            

            user_chat['search_query'] = ' '.join(map(lambda x: x.capitalize(),
                                                 update.text.split(' ')))
            user_chat['link'] = None
            command_get_specify_apk(bot, update)
        else:
            home_string = "{}".format("start")
            bot.edit_message_text(text="This action is not supported :(",
                         chat_id=update.from_user.id,
                         message_id=update.message.message_id,
                         reply_markup=InlineKeyboardMarkup(
        [
          
            [  
                InlineKeyboardButton("⬅️ Go Back", callback_data=home_string.encode("UTF-8")),
            ]
        ]
    ))

@app.on_message(Filters.command("start"))    
def start(bot, update):
    global active_chats
    active_chats[update.from_user.id] = {'actions': []}
    audio_string = "{}".format("downl")
    
    video_string = "{}".format("other")
    
    info_string = "{}".format("help")
    
    join_string = "{}".format("join")
    
  
    sent = bot.send_message(update.chat.id, 
        text=Translation.START_TEXT,
        reply_markup=InlineKeyboardMarkup(
        [
            [  # First row
                # Generates a callback query when pressed
                InlineKeyboardButton("⬇️ Download Tool", callback_data=audio_string.encode("UTF-8")),
                # Opens a web URL
                InlineKeyboardButton("♻️ Other Projects", callback_data=video_string.encode("UTF-8")),
            ],
            [  
                InlineKeyboardButton("🚸 Join Beta group ", callback_data=join_string.encode("UTF-8")),
            ],
            [  
                InlineKeyboardButton("🆘 Help and Usage", callback_data=info_string.encode("UTF-8")),
            ]
        ]
    ),
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True).message_id
    

@app.on_message(Filters.text | Filters.regex("!apkw"))
def apk(client, message):
  global active_chats
  active_chats[message.from_user.id] = {'actions': []}
  audio_string = "{}".format("downl")
  if message.text.startswith('/apkw') or message.text.startswith('!apkw'):
      first_time = time.time()
      word = message.text[4:]
      search = " ".join(word)
      if word == '':
        client.send_message(message.chat.id,'**Usage:** `!apk name or package name`', reply_to_message_id=message.message_id)
      else: 
        sent = client.send_message(message.chat.id, fetching_download_link.format(search), reply_to_message_id=message.message_id).message_id 
        ress = requests.get('https://apkpure.com/search?q={}&region='.format(quote_plus(search)), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5'}).text 
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
        res = requests.get(link + '/download?from=details', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5'}).text
        soup = BeautifulSoup(res, "html.parser").find('a', {'id': 'download_link'})
        if soup['href']:
          r = requests.get(soup['href'], stream=True, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5'})
          required_file_name = get_filename_from_cd(r.headers.get('content-disposition'))
          with open(required_file_name, 'wb') as apk:
            for chunk in r.iter_content(chunk_size=8192):
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
        try:
          client.delete_messages(message.chat.id, sent)
          client.delete_messages(message.chat.id, message.message_id)
        except pyrogram.api.errors.exceptions.forbidden_403.MessageDeleteForbidden as E:
          client.send_message(message.chat.id, str(E), reply_to_message_id=message.message_id)
          pass
        t1 = time.time()
        client.send_chat_action(message.chat.id,'UPLOAD_DOCUMENT')
        sent = client.send_document(message.chat.id, required_file_name, caption="File Upload Sucessfull", reply_to_message_id=message.message_id).message_id
        time.sleep(5)
        t2 = time.time()
        description = " " + " \r\n© Made with ❤️ by @Bfas237Bots "
        client.edit_message_caption(message.chat.id,sent,caption='**File Size**: {}\n\n**Completed in**:  `{}` **Seconds**\n'.format(str(pretty_size(total_length)), str(int(t2-t1))))
        time.sleep(3)
        client.edit_message_caption(message.chat.id,sent,caption='\n{}\n'.format(description))
        os.remove(required_file_name)

@app.on_callback_query(dynamic_data("start"))
def start_data(bot, update):
    global active_chats
    active_chats[update.from_user.id] = {'actions': []}
    audio_string = "{}".format("downl")
    
    video_string = "{}".format("other")
    
    info_string = "{}".format("help")
    
    join_string = "{}".format("join")
    
  
    
    bot.edit_message_text(
        chat_id=update.from_user.id,
        text=Translation.START_TEXT,
        reply_markup=InlineKeyboardMarkup(
        [
            [  # First row
                # Generates a callback query when pressed
                InlineKeyboardButton("⬇️ Download Tool", callback_data=audio_string.encode("UTF-8")),
                # Opens a web URL
                InlineKeyboardButton("♻️ Other Projects", callback_data=video_string.encode("UTF-8")),
            ],
            [  
                InlineKeyboardButton("🚸 Join Beta group ", callback_data=join_string.encode("UTF-8")),
            ],
            [  
                InlineKeyboardButton("🆘 Help and Usage", callback_data=info_string.encode("UTF-8")),
            ]
        ]
    ),
        message_id=update.message.message_id,
        disable_web_page_preview=True
    
    )

    
@app.on_callback_query(dynamic_data("join"))
def pyrogram_data(bot, update):
    global active_chats
    if update.from_user.id not in active_chats:
        active_chats[update.from_user.id] = {'actions': []}
    active_chats[update.from_user.id]['actions'].append('join')
    
    
    start_string = "{}".format("start")
    bot.edit_message_text(
        text="⚠️ Please Before you join the group bare in mind that its not a group to spam with links and sfw. Hope you understand",
        chat_id=update.from_user.id,
        reply_markup=InlineKeyboardMarkup(
        [
            [  # First row
                # Generates a callback query when pressed
                InlineKeyboardButton("🚹  Join Beta group" , url="https://t.me/joinchat/C74PmEPu2JymxxnUCbPytw"),
                # Opens a web URL
                InlineKeyboardButton("⬅️  Retrun to Main menu" , callback_data=start_string.encode("UTF-8")),
            ],
        
        
        ]
    ),
        message_id=update.message.message_id
    )          
@app.on_callback_query(dynamic_data("downl"))
def pyrogram_data(bot, update):
    global active_chats
    if update.from_user.id not in active_chats:
      active_chats[update.from_user.id] = {'actions': []}
    active_chats[update.from_user.id]['actions'].append('downl')
    
    start_string = "{}".format("start")
    apk_string = "{}".format("apks")
    vid_string = "{}".format("vid")
    aud_string = "{}".format("aud")
    bot.edit_message_text(
        text="🆑 Here you can perform download actions. This section permits you to download android apps for free.\n\n Have fun",
        chat_id=update.from_user.id,
        reply_markup=InlineKeyboardMarkup(
        [
            [  # First row
                # Generates a callback query when pressed
                InlineKeyboardButton("🚧 Download Android Apps " , callback_data=apk_string.encode("UTF-8"))
            ],
            [ 
                InlineKeyboardButton("🚫  Abort Process" , callback_data=start_string.encode("UTF-8"))
            ]
        
        
        ]
    ),
        message_id=update.message.message_id
    ) 
@app.on_callback_query(dynamic_data("apks"))
def pyrogram_data(bot, update):
    global active_chats
    if update.from_user.id not in active_chats:
        active_chats[update.from_user.id] = {'actions': []}
    active_chats[update.from_user.id]['actions'].append('apks')
    
    
    start_string = "{}".format("downl")
    bot.edit_message_text(
        text="**📱 Apk Downloader Premium**\n\n__Step 1 of  3__\n"
                              "\nOK! Send me search query in next message.",
        chat_id=update.from_user.id,
        reply_markup=InlineKeyboardMarkup(
        [
            [  
                # Opens a web URL
                InlineKeyboardButton("⬅️  Retrun to Previous menu" , callback_data=start_string.encode("UTF-8")),
            ],
        
        
        ]
    ),
        message_id=update.message.message_id
    )    
def command_get_specify_apk(bot, update):
    if active_chats.get(update.from_user.id).get('link') is None:
      search_query = active_chats.get(update.from_user.id).get('search_query')
    searchs = " ".join(search_query) 
    sent = bot.send_message(update.chat.id, 
        text=fetching_download_link.format(searchs),
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True)
    print('Searching for: {}'.format(searchs))
    search(searchs)
    time.sleep(5)
    if len(APPS) == 0:
      bot.edit_message_text(text='Your search returned No results',
                         chat_id=update.message.chat_id,
                         parse_mode="Markdown",
                         message_id=update.message.chat_id,
                         #reply_markup=reply_markup,
                         disable_web_page_preview=True)
      return
      
    
    inline_keyboard = []
    if len(APPS) > 0:
      for idx, app in enumerate(APPS):
        
        start_string = "{}|{}".format(idx, app[0])
        ikeyboard = [
                            InlineKeyboardButton(
                                "[{:02d}]  -  {}".format(idx, app[0]),
                                callback_data=start_string.encode("UTF-8")
                            )
                        ]
        user_chat = active_chats.get(update.from_user.id, None)
        user_chat['Aps'] = APPS
        user_chat['Apps'] = None        
        inline_keyboard.append(ikeyboard)
        num=len(APPS)
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        bot.edit_message_text(
        text="🔍 Search for **{}** Returned (`{}`) results\n\n Click on your app and i will download it right away".format(search_query, num),
        chat_id=update.from_user.id,
        
        reply_markup=reply_markup,
        message_id=sent.message_id,
        disable_web_page_preview=True)
        
@app.on_callback_query(dynamic_data("help"))
def pyrogram_data(bot, update):
    global active_chats
    if update.from_user.id not in active_chats:
        active_chats[update.from_user.id] = {'actions': []}
    active_chats[update.from_user.id]['actions'].append('help')
    
    
    start_string = "{}".format("start")
    bot.edit_message_text(
        text=Translation.HELP_TEXT,
        chat_id=update.from_user.id,
        
        reply_markup=InlineKeyboardMarkup(
        [
            
            [  
                InlineKeyboardButton("⬅️ " + "Go Back" , callback_data=start_string.encode("UTF-8"))
            ]
        ]
    ),
        message_id=update.message.message_id
    )        
    
            
@app.on_callback_query(dynamic_data("getapk"))
def pyrogram_data(bot, update):
    if active_chats.get(update.from_user.id).get('link') is None:
      search_query = active_chats.get(update.from_user.id).get('search_query')
    searchs = " ".join(search_query) 
    sent = bot.send_message(update.from_user.id, fetching_download_link.format(searchs), reply_to_message_id=update.message.message_id).message_id 
    print('Searching for: {}'.format(searchs))
    search(searchs)
    time.sleep(5)
    if len(APPS) == 0:
      bot.edit_message_text(text='Your search returned No results',
                         chat_id=update.message.chat_id,
                         parse_mode="Markdown",
                         message_id=update.message.chat_id,
                         #reply_markup=reply_markup,
                         disable_web_page_preview=True)
      return
    
    bot.delete_messages(update.from_user.id, update.message.message_id)
    inline_keyboard = []
    if len(APPS) > 0:
      for idx, app in enumerate(APPS):
        
        start_string = "{}|{}".format(idx, app[0])
        ikeyboard = [
                            InlineKeyboardButton(
                                "[{:02d}]  -  {}".format(idx, app[0]),
                                callback_data=start_string.encode("UTF-8")
                            )
                        ]
        user_chat = active_chats.get(update.from_user.id, None)
        user_chat['Aps'] = APPS
        user_chat['Apps'] = None        
        inline_keyboard.append(ikeyboard)
        num=len(APPS)
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        bot.edit_message_text(
        text="🔍 Search for *{}* Returned (`{}`) results\n\n Click on your app and i will download it right away".format(search_query, num),
        chat_id=update.from_user.id,
        
        reply_markup=reply_markup,
        message_id=sent,
        disable_web_page_preview=True
    )        

def save_photo(bot, update):
    if str(update.from_user.id) not in Config.AUTH_USERS:
        bot.send_message(
            chat_id=update.from_user.id,
            text=Translation.NOT_AUTH_USER_TEXT,
            reply_to_message_id=update.message_id
        )
        return
    download_location = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    bot.download_media(
        message=update,
        file_name=download_location
    )
    bot.send_message(
        chat_id=update.from_user.id,
        text=Translation.SAVED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id
    )


def download(link, options={}):
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass
    base_headers = {
        'User-Agent':  ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    headers = dict(base_headers, **options)
    try:
        res = requests.get(link + '/download?from=details', headers=headers).text
        soup = BeautifulSoup(res, "html.parser").find('a', {'id':'download_link'})
        if soup['href']:
            r = requests.get(soup['href'], stream=True, headers=headers)
            required_file_name = get_filename_from_cd(r.headers.get('content-disposition'))
            with open(link.split('/')[-1] + '.apk', 'wb') as file:
                for chunk in r.iter_content(chunk_size=8192):
                    total_length = r.headers.get('content-length')
                    dl = 0
                    total_length = int(total_length)
                    if chunk:
                        dl += len(chunk)
                        done = int(100 * dl / total_length)
                        file.write(chunk)
                        file.flush()
    except (ProtocolError, ConnectionError, ConnectionResetError, ReadTimeout, Timeout, TimeoutError, ConnectTimeout) as e:
        bot.send_message(
            chat_id=update.from_user.id,
            text=e,
            reply_to_message_id=update.message_id
        )
        return None
def button(bot, update):
    
    if active_chats.get(update.from_user.id).get('Apps') is None:
      APPS = active_chats.get(update.from_user.id).get('Aps')
    if str(update.from_user.id) not in Config.AUTH_USERS:
        bot.send_message(
            chat_id=update.from_user.id,
            text=Translation.NOT_AUTH_USER_TEXT,
            reply_to_message_id=update.message_id
        )
        return
      
      
    
    rnd = "123456789abcdefgh-_"
    servers = shuffle(rnd)  
    if update.data.find("|") == -1:
        return ""
    app_num, app_name = update.data.split("|")
    app_num = int(app_num)
    options={}
    link = APPS[app_num][2]
    first_time = time.time()
    bot.edit_message_text(update.from_user.id, update.message.message_id, download_job_started.format(servers, APPS[app_num][2]))
    time.sleep(5)
    print('Downloading {}.apk ...'.format(link.split('/')[-1]))
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass
    base_headers = {
        'User-Agent':  ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    headers = dict(base_headers, **options)
    try:
        res = requests.get(link + '/download?from=details', headers=headers).text
        soup = BeautifulSoup(res, "html.parser").find('a', {'id':'download_link'})
        if soup['href']:
            r = requests.get(soup['href'], stream=True, headers=headers)
            required_file_name = get_filename_from_cd(r.headers.get('content-disposition'))
            with open(required_file_name, 'wb') as file:
                for chunk in r.iter_content(chunk_size=8192):
                    total_length = r.headers.get('content-length')
                    dl = 0
                    total_length = int(total_length)
                    if chunk:
                        dl += len(chunk)
                        done = int(100 * dl / total_length)
                        file.write(chunk)
                        file.flush()
    except (ProtocolError, ConnectionError, ConnectionResetError, ReadTimeout, Timeout, TimeoutError, ConnectTimeout) as Error:
        bot.edit_message_text(update.from_user.id, update.message.message_id, Error)
        return None
    time.sleep(5)
    second_time = time.time()
    print('Download complete .......')
    bot.edit_message_text(update.from_user.id, update.message.message_id, download_successfull.format(str(second_time - first_time)[:5]))
    time.sleep(5)
    bot.edit_message_text(update.from_user.id, update.message.message_id, upload_job_started)
    bot.delete_messages(update.from_user.id, update.message.message_id)
    t1 = time.time()
    file_size = os.stat(required_file_name).st_size
    bot.send_chat_action(update.from_user.id,'UPLOAD_DOCUMENT')
    sent = bot.send_document(update.from_user.id, required_file_name, caption="File Upload Sucessfull", reply_to_message_id=update.message.reply_to_message.message_id)
    time.sleep(5)
    t2 = time.time()
    description = " " + " \r\n© Made with ❤️ by @Bfas237Bots "
    bot.edit_message_caption(update.from_user.id,sent.message_id,caption='**File Size**: {}\n\n**Completed in**:  `{}` **Seconds**\n'.format(str(pretty_size(total_length)), str(int(t2-t1))))
    time.sleep(3)
    bot.edit_message_caption(update.from_user.id,sent.message_id,caption='\n{}\n'.format(description))
    os.remove(required_file_name)

        
        

if __name__ == "__main__" :
    # create download directory, if not exist
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    app.add_handler(pyrogram.MessageHandler(start, pyrogram.Filters.command(["start"])))
    app.add_handler(pyrogram.MessageHandler(apk, pyrogram.Filters.text))
    app.add_handler(pyrogram.MessageHandler(messages, pyrogram.Filters.text))
    app.add_handler(pyrogram.MessageHandler(save_photo, pyrogram.Filters.photo))
    app.add_handler(pyrogram.CallbackQueryHandler(button))
    app.run()
