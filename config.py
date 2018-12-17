from pyrogram import Client

## Bot settings ##
import os
api_id = 256406
api_hash = "31fd969547209e7c7e23ef97b7a53c37"
class Config(object):
    # get a token from https://chatbase.com
    CHAT_BASE_TOKEN = os.environ.get("CHAT_BASE_TOKEN", "880f05a1-685c-4909-a8f6-b17463625eba")
    # get a token from @BotFather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "671045549:AAGcbv7YKKQdUIjTnMmrEg46AGgyJmnLtFg")
    # your domain to show when download file is greater than MAX_FILE_SIZE
    HTTP_DOMAIN = os.environ.get("HTTP_DOMAIN", "https://bfbr0.herokuapp.com/")
    # for running on Heroku.com
    PORT = int(os.environ.get('PORT', 5000))
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", api_id))
    API_HASH = os.environ.get("API_HASH", api_hash)
    # Get these values from my.telegram.org
    # the download location, where the HTTP Server runs
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    # Telegram maximum file upload size
    MAX_FILE_SIZE = 400000000
    TG_MAX_FILE_SIZE = 14000000000
    # chunk size that should be used with requests
    CHUNK_SIZE = 100*1024


language = "english"

app = Client(
    "671045549:AAGcbv7YKKQdUIjTnMmrEg46AGgyJmnLtFg",
    api_id=api_id,
    api_hash=api_hash
)

# Automatically sets your user id

app.start()
user_id = app.get_me().id
app.stop()

# Set an error channel

log_channel = -1001249303594

# Enabled plugins

plugins = [
    "eval", 
    "exec", 
    "info", 
    "purgeme", 
    "urban", 
    "bash", 
    "restart", 
    "filtext", 
    "haste"
]

# Command prefix

prefix = "!"
