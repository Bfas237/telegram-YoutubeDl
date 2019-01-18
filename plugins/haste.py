from pyrogram import Filters
import config
import requests

app = config.app
user_id = config.user_id


if config.language == "english":
    from languages.english import eval_running_text, eval_error_text, eval_success_text, eval_result_text

RUNNING = "**Uploading to:** a paste center for you"
ERROR = "**There was a glitch:**\n```{}```\n**Error:**\n```{}```"
NoSUCCESS = "**Sorry i had to end unexpectedly:**\n```{}```\n**None**"
RESULT = "**Result:**\n{}"
https://hastebin.com/

@app.on_message(Filters.command("paste", prefix="!"))
def paste(client, message):
    haste = " ".join(message.command[1:])

    if haste:
        if message.reply_to_message:
            m = message.reply(RUNNING.format(haste))

        try:
            result = requests.post("https://hastebin.com/documents", data=content.encode('utf-8'))
        except Exception as error:
            client.edit_message_text(
                m.chat.id,
                m.message_id,
                ERROR.format(haste, error)
            )
        else:
            if not result:
                client.edit_message_text(
                    m.chat.id,
                    m.message_id,
                    NoSUCCESS.format(haste)
                )
            else:
                go = "https://hastebin.com/" + post.json()["key"]
                client.edit_message_text(
                    m.chat.id,
                    m.message_id,
                    RESULT.format(go)
                )
