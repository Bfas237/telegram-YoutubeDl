from pyrogram import Client

## Bot settings ##

api_id = 256406
api_hash = "31fd969547209e7c7e23ef97b7a53c37"
language = "english"

app = Client(
    "account",
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

plugins = ["eval", "exec", "info", "purgeme", "urban", "bash", "restart"]

# Command prefix

prefix = "!"
