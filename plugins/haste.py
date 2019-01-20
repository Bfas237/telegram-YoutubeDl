from pyrogram import Filters
import config
import requests

app = config.app
user_id = config.user_id


from pyrogram import Client, Filters
    
@app.on_message(Filters.command("r", prefix="!") & Filters.reply & ~Filters.edited & Filters.group)
def r(client, message):
    if len(message.command) > 1:
        colength = len("r") + len("!")
        query = str(message.text)[colength:].lstrip()
        eventsplit=query.split("/")
        result="**You mean:**\n{}".format(message.reply_to_message.text.replace(eventsplit[0],eventsplit[1]))
        client.edit_message_text(message.chat.id, message.message_id, result)
