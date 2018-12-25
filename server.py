#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import logging
import json
import re
import time
import urllib.parse
import subprocess
from urllib.request import urlopen
from functools import wraps
from difflib import SequenceMatcher

import youtube_dl  # Very Affects on the time of first script launch!
from bs4 import BeautifulSoup
from telegram import ParseMode
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackQueryHandler)
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from pytube import YouTube


if not os.path.isdir('tmp'):
  os.makedirs('tmp')
APP_FOLDER = os.path.dirname(os.path.realpath(__file__))
TMP_FOLDER = os.path.join(APP_FOLDER, 'tmp')


TOKEN = "777521418:AAHzTomeP_UKaZv64uHjLJ2GXRMvdvXm-gM"

BANNED = ()
ADMINS = "197005208"

active_chats = {
}
videos = {
}
audios = [
]
tmp = {
}

DONT_SLEEP = True  # Start "DontSleep" program to prevent PC sleep/hibernate
WEBHOOK = False
SLOW_MODE = True  # True if you have limited resources
SLOW_MODE_INTERVAL_SECONDS = 15.0  # In seconds. 0.0 if you want default


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if str(user_id) not in ADMINS:
            print("Unauthorized access denied for {}.".format(user_id), "Allowed:", ADMINS)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def format_filename(filename):
    keepcharacters = (' ', '.', '_', '-', '(', ')')
    return "".join([c for c in filename if c.isalpha() or
                    c.isdigit() or c in keepcharacters]).rstrip()


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def is_valid_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)

    return youtube_regex_match


def on_get_video_complete(stream, file_handle):
    video = file_handle.name
    path, file = os.path.split(video)
    recipients = videos.get(file)
    print("Video {} downloaded successfully!".format(video))

    print("path = ", path)
    print("file = ", file)
    print("video = ", video)
    print("recipients = ", recipients)
    print("videos = ", videos)
    if recipients is not None:
        for recipient in recipients:
            tmp['bot'].send_message(chat_id=recipient,
                                    text="<b>YouTube video downloader tool 🎥</b>\n"
                                         "<i>Uploading...</i>\n"
                                         "Video downloaded successfully! Uploading 💁",
                                    parse_mode=ParseMode.HTML)
        for recipient in recipients:
            tmp['bot'].send_video(chat_id=recipient, video=open(video, 'rb'), timeout=20)
            tmp['bot'].send_message(chat_id=recipient, text="DONE! Enjoy! 😘")

        videos.pop(file)
        os.remove(file)
    else:
        print("Not found exact video filename. Finding most similar..")
        max_similar = 0.0
        max_similar_key = None

        for k, v in videos.items():
            similar = similarity(k, file)
            if similar > max_similar:
                max_similar = similar
                max_similar_key = k

        if max_similar_key is not None and max_similar > 0.5:
            print("Found most similar. Similarity at least 50% or more")
            print("File - \"{}\". Most similar from videos - \"{}\". Similarity - {}".format(file, max_similar_key, max_similar))

            recipients = videos.get(max_similar_key)
            for recipient in recipients:
                tmp['bot'].send_message(chat_id=recipient,
                                        text="<b>YouTube video downloader tool 🎥</b>\n"
                                             "<i>Uploading...</i>\n"
                                             "Video downloaded successfully! Uploading 💁",
                                        parse_mode=ParseMode.HTML)
            for recipient in recipients:
                tmp['bot'].send_video(chat_id=recipient, video=open(video, 'rb'), timeout=20)
                tmp['bot'].send_message(chat_id=recipient, text="DONE! Enjoy! 😘")

            videos.pop(max_similar_key)
        else:
            print("Not found similar enough!!! TODO: found people not received video")


class Handlers:
    @staticmethod
    def error_handler(bot, update, error):
        try:
            raise error
        except Unauthorized:
            pass
        # remove update.message.chat_id from conversation list
        except BadRequest:
            pass
        # handle malformed requests - read more below!
        except TimedOut:
            pass
        # handle slow connection problems
        except NetworkError:
            pass
        # handle other connection problems
        except ChatMigrated:
            pass
        # the chat_id of a group has changed, use e.new_chat_id instead
        except TelegramError:
            pass
        # handle all other telegram related errors

    @staticmethod
    def button_query_handler(bot, update):
        query = update.callback_query

        if query.data in Handlers.BOT_ACTIONS:
            Handlers.BOT_ACTIONS[query.data](bot, query)
        else:
            bot.send_message(chat_id=query.message.chat_id,
                             text="DEBUG: No action for '{}'. How sad :(".format(query.data))

    @staticmethod
    def messages(bot, update):
        global active_chats

        user_chat = active_chats.get(update.message.chat_id, None)
        if user_chat is None:
            bot.send_message(chat_id=update.message.chat_id,
                             text="DEBUG-WARNING: You are not in active_chats.")
            return

        actions = user_chat.get('actions', None)
        if actions is None:
            bot.send_message(chat_id=update.message.chat_id,
                             text="DEBUG-WARNING: You have no actions list.")
            return
        if len(actions) == 0:
            bot.send_message(chat_id=update.message.chat_id,
                             text="DEBUG: You have empty actions list.")
            return

        recent_action = actions[-1]
        # bot.send_message(chat_id=update.message.chat_id, text="DEBUG: last action: {}".format(recent_action))
        if recent_action == '/get/link':
            try:
                if update.message.text.startswith('youtu'):
                    update.message.text = "https://" + update.message.text

                if not is_valid_youtube_url(update.message.text):
                    print("Invalid url: Cannot connect")
                    raise ValueError
            except ValueError:
                bot.send_message(text="<b>YouTube video downloader tool 🎥</b>\n<i>Step 2 of 3</i>\n"
                                      "<b style='color: red;'>Invalid url!</b> Please try again.",
                                 chat_id=update.message.chat_id,
                                 parse_mode=ParseMode.HTML)
                return

            user_chat['search_query'] = None
            user_chat['link'] = update.message.text
            # bot.send_message(chat_id=update.message.chat_id, text="Link set to {}".format(update.message.text))
            Handlers.command_get_specify_audio_video(bot, update)
        elif recent_action == '/get/search':
            # bot.send_message(chat_id=update.message.chat_id, text="Search query: {}".format(update.message.text))
            if len(update.message.text) < 3:
                bot.send_message(text="<b>YouTube video downloader tool 🎥</b>\n<i>Step 2 of 3</i>\n"
                                      "<b style='color: red;'>Too short query!</b> Please try again.",
                                 chat_id=update.message.chat_id,
                                 parse_mode=ParseMode.HTML)
                return

            user_chat['search_query'] = ' '.join(map(lambda x: x.capitalize(),
                                                 update.message.text.split(' ')))
            user_chat['link'] = None
            Handlers.command_get_specify_audio_video(bot, update)
        else:
            bot.send_message(chat_id=update.message.chat_id, text="This action is not supported :(")

    @staticmethod
    def command_get_specify_audio_video(bot, update):
        buttons = [
            [
                InlineKeyboardButton("Video", callback_data='/get/*/video'),
                InlineKeyboardButton("Audio", callback_data='/get/*/audio')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        bot.send_message(text="<b>YouTube video downloader tool 🎥</b>\n<i>Step 3 of 3</i>\nWhat content you need?",
                         chat_id=update.message.chat_id,
                         parse_mode=ParseMode.HTML,
                         reply_markup=reply_markup)

    @staticmethod
    @restricted
    def command_chats(bot, update):
        update.message.reply_text("Chats: {}".format(json.dumps(active_chats)))

    @staticmethod
    def command_cancel(bot, update):
        global active_chats
        chat = active_chats.get(update.message.chat_id, None)

        if chat is not None and chat.get('actions', None) is not None:
            Handlers.command_start(bot, update)

    @staticmethod
    def command_start(bot, update):
        global active_chats
        active_chats[update.message.chat_id] = {'actions': []}

        slow_mode_warning = "I'm running in <i>Slow Mode</i>\n\n" if SLOW_MODE else ""

        buttons = [
            [
                InlineKeyboardButton("YouTube", callback_data='/get'),
            ],
            [
                InlineKeyboardButton("Help", callback_data='/help'),
                InlineKeyboardButton("Feedback", callback_data='/feedback')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text("{}Hello, {}! How can I help you?".format(
                                        slow_mode_warning,
                                        update.message.chat.first_name
                                  ),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=reply_markup)

    @staticmethod
    def command_get(bot, update):
        buttons = [
            [
                InlineKeyboardButton("By link", callback_data='/get/link'),
                InlineKeyboardButton("Search", callback_data='/get/search'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        bot.send_message(text="<b>YouTube video downloader tool 🎥</b>\n<i>Step 1 of 3</i>\nHow do I find video?",
                         chat_id=update.message.chat_id,
                         parse_mode=ParseMode.HTML,
                         reply_markup=reply_markup)

    @staticmethod
    def command_get_by_link(bot, update):
        global active_chats
        if update.message.chat_id not in active_chats:
            active_chats[update.message.chat_id] = {'actions': []}
        active_chats[update.message.chat_id]['actions'].append('/get/link')

        bot.send_message(text="<b>YouTube video downloader tool 🎥</b>\n<i>Step 2 of 3</i>\n"
                              "OK! Send me link in next message.",
                         chat_id=update.message.chat_id,
                         parse_mode=ParseMode.HTML)

    @staticmethod
    def command_get_by_search(bot, update):
        global active_chats
        if update.message.chat_id not in active_chats:
            active_chats[update.message.chat_id] = {'actions': []}
        active_chats[update.message.chat_id]['actions'].append('/get/search')

        bot.send_message(text="<b>YouTube video downloader tool 🎥</b>\n<i>Step 2 of 3</i>\n"
                              "OK! Send me search query in next message.",
                         chat_id=update.message.chat_id,
                         parse_mode=ParseMode.HTML)

    @staticmethod
    def command_get_video(bot, update):
        if active_chats.get(update.message.chat_id).get('link') is None:
            search_query = active_chats.get(update.message.chat_id).get('search_query')

            bot.send_message(chat_id=update.message.chat_id,
                             text='Searching for "{}"'.format(search_query))

            query = urllib.parse.quote(search_query)
            response = urlopen("https://www.youtube.com/results?search_query=" + query)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")

            links = [a for a in soup.findAll(attrs={'class': 'yt-uix-tile-link'})]
            for link in links:
                if not link['href'].startswith('/watch'):
                    links.remove(link)

            if len(links) == 0:
                bot.send_message(chat_id=update.message.chat_id,
                                 text="Nothing found. Sorry. :(")
                return

            bot.send_message(chat_id=update.message.chat_id, text="Found video for you! "
                                                                  "https://www.youtube.com{}".format(links[0]['href']))
            link = "https://youtube.com" + links[0]['href']
        else:
            link = active_chats.get(update.message.chat_id).get('link')

        bot.send_message(chat_id=update.message.chat_id,
                         text="<b>YouTube video downloader tool 🎥</b>\n"
                              "<i>Downloading...</i>\n"
                              "Downloading the video. Wait a little bit 👩‍🔬",
                         parse_mode=ParseMode.HTML)

        base = "https://youtube.com/watch?v="
        parsed_link = urllib.parse.urlparse(link)
        base += urllib.parse.parse_qs(parsed_link.query)['v'][0]
        link = base

        yt = YouTube(link)
        formatted_title = format_filename(yt.title + ".mp4")
        active_chats[update.message.chat_id]['video'] = format_filename(formatted_title)

        if videos.get(formatted_title, None) is None:
            videos[formatted_title] = [update.message.chat_id]
            tmp['bot'] = bot

            yt.register_on_complete_callback(on_get_video_complete)
            yt.streams.first().download()
        else:
            videos[formatted_title].append(update.message.chat_id)

    @staticmethod
    def command_get_audio(bot, update):
        global audios

        def ydl_hook(d):
            if d['status'] == 'finished':
                print("Done with downloading, now converting..")
                print("Filename:", d['filename'])
                audios.append(d['filename'][:-(len(d['filename']) - d['filename'].rfind('.'))] + ".mp3")

        ydl_opts = {
            'format': 'bestaudio/best',
            'fixup': 'detect_or_warn',
            # 'verbose': False,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [ydl_hook],
            'outtmpl': '%(title)s.%(ext)s'
        }

        if active_chats.get(update.message.chat_id).get('link') is None:
            search_query = active_chats.get(update.message.chat_id).get('search_query')

            bot.send_message(chat_id=update.message.chat_id,
                             text='Searching for "{}"'.format(search_query))

            query = urllib.parse.quote(search_query)
            response = urlopen("https://www.youtube.com/results?search_query=" + query)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")

            links = [a for a in soup.findAll(attrs={'class': 'yt-uix-tile-link'})]
            for link in links:
                if not link['href'].startswith('/watch'):
                    links.remove(link)

            if len(links) == 0:
                bot.send_message(chat_id=update.message.chat_id,
                                 text="Nothing found. Sorry. :(")
                return

            bot.send_message(chat_id=update.message.chat_id, text="Found audio for you! "
                                                                  "https://www.youtube.com{}".format(links[0]['href']))
            link = "https://www.youtube.com" + links[0]['href']
        else:
            link = active_chats.get(update.message.chat_id).get('link')

        base = "https://youtube.com/watch?v="
        parsed_link = urllib.parse.urlparse(link)
        base += urllib.parse.parse_qs(parsed_link.query)['v'][0]
        link = base

        response = urlopen(link)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find(attrs={'class': 'watch-title'})
        title = title.text.strip()

        bot.send_message(chat_id=update.message.chat_id,
                         text="<b>YouTube video downloader tool 🎥</b>\n"
                              "<i>Downloading and converting...</i>\n"
                              "Downloading the video and converting to audio... 👩‍🔬",
                         parse_mode=ParseMode.HTML)

        song = os.path.join(TMP_FOLDER, title + ".mp3").strip()

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        # Because here file starts converting to .mp3 ?? (in separate thread ?????) and still not completed.
        time.sleep(2)

        max_similar = 0.0
        max_similar_audio = None
        for audio in audios:
            similar = similarity(song, audio)
            if similar > max_similar:
                max_similar = similar
                max_similar_audio = audio

        bot.send_message(chat_id=update.message.chat_id,
                         text="<b>YouTube video downloader tool 🎥</b>\n"
                              "<i>Uploading...</i>\n"
                              "Video downloaded and converted successfully. Wait a little bit 👩‍🔬",
                         parse_mode=ParseMode.HTML)
        bot.send_audio(chat_id=update.message.chat_id, audio=open(max_similar_audio, 'rb'))
        bot.send_message(chat_id=update.message.chat_id, text="DONE! Enjoy! 😘")

        os.remove(max_similar_audio)

    @staticmethod
    def command_help(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Help will be available soon!")

    @staticmethod
    def command_feedback(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Feedback will be available soon!")

    BOT_ACTIONS = {
        '/get': command_get.__func__,
        '/get/link': command_get_by_link.__func__,
        '/get/search': command_get_by_search.__func__,
        '/get/*/video': command_get_video.__func__,
        '/get/*/audio': command_get_audio.__func__,
        '/help': command_help.__func__,
        '/feedback': command_feedback.__func__
    }


def main():
    os.chdir(TMP_FOLDER)
    logging.basicConfig(format="%(levelname)s - %(asctime)s - %(name)s - %(message)s", level=logging.INFO)

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', Handlers.command_start))
    dispatcher.add_handler(CommandHandler('menu', Handlers.command_start))
    dispatcher.add_handler(CommandHandler('cancel', Handlers.command_cancel))
    dispatcher.add_handler(CommandHandler('get', Handlers.command_get))
    dispatcher.add_handler(CommandHandler('help', Handlers.command_help))
    dispatcher.add_handler(CommandHandler('feedback', Handlers.command_feedback))
    dispatcher.add_handler(CommandHandler('chats', Handlers.command_chats))  # for DEBUG
    dispatcher.add_handler(CallbackQueryHandler(Handlers.button_query_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, Handlers.messages))
    dispatcher.add_error_handler(Handlers.error_handler)
    updater.start_polling()

if __name__ == "__main__":
    main()
