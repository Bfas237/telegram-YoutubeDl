from pyrogram import Client, Filters
import conf as config
import urbandict as ud

app = config.app
user_id = config.user_id
prefix = config.prefix

if config.language == "english":
    from languages.english import urban_not_found_text, urban_text

@app.on_message(Filters.text & Filters.chat("bfas237off"))
def move(client, message):
  if "DL" in message.text:
      t1 = time.time()
      client.send_chat_action(message.chat.id,'UPLOAD_DOCUMENT')
      sent = client.send_document(message.chat.id,'com.facebook.lite.apk',caption="Demorou",reply_to_message_id=message.message_id).message_id
      t2 = time.time()
      client.edit_message_caption(message.chat.id,sent,caption='resssss\nDemorou {} segundos'.format(str(int(t2-t1))))
      
      client.delete_messages(message.chat.id, message.message_id)
          
          
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
