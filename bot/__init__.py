import logging
from os import getenv, mkdir

from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

if getenv("DEBUG"):
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.WARN)

# Base bot info
ADMINS = getenv("ADMINS").split()
BASE_FOLDER = getenv("DOWNLOAD_FOLDER", "/data")
DL_FOLDER = BASE_FOLDER

# Telegram login info
BOT_TOKEN = getenv("BOT_TOKEN")
PHONE_NUMBER = getenv("PHONE_NUMBER")
TAPI_ID = int(getenv("TELEGRAM_API_ID"))
TAPI_HASH = getenv("TELEGRAM_API_HASH")

try:
    mkdir(DL_FOLDER)
except FileExistsError:
    pass
except:
    logging.error("Failed to create data storage path!")
    exit(1)

app = Client("TDownloader-bot", TAPI_ID, TAPI_HASH, bot_token=BOT_TOKEN)

user = None
if PHONE_NUMBER:
    user = Client("TDownloader-user", TAPI_ID, TAPI_HASH, phone_number=PHONE_NUMBER)
