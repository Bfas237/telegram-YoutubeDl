from pyrogram import Client

## Bot settings ##
import os

class Config(object):
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    # Telegram maximum file upload size
    MAX_FILE_SIZE = 400000000
    TG_MAX_FILE_SIZE = 14000000000
    # chunk size that should be used with requests
    CHUNK_SIZE = 100*1024


language = "english"

app = Client(
    os.environ.get("TOKEN"),
    api_id=os.environ["APP_ID"],
    api_hash=os.environ["API_HASH"])

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
