from pyrogram import Filters
import config
import requests
BASE = "https://hastebin.com"
app = config.app
user_id = config.user_id


from pyrogram import Client, Filters
    
@app.on_message(Filters.command("hb", prefix="!") & Filters.reply)
def eval_expression(client, message):
    expression = " ".join(message.command[1:])
    reply = message.reply_to_message

    if reply.text is None:
        return

    message.delete()

    result = requests.post(
        "{}/documents".format(BASE),
        data=reply.text.encode("UTF-8")
    ).json()

    message.reply(
        "{}/{}.py".format(BASE, result["key"]),
        reply_to_message_id=reply.message_id
    )
