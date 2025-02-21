import logging
from os import getenv, mkdir

from dotenv import load_dotenv
from pyrogram.client import Client

load_dotenv()

if getenv("DEBUG"):
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.WARN)


MAX_SIMULTANEOUS_TRANSMISSIONS = 3

# Base bot info
ADMINS = getenv("ADMINS", "").split()
BASE_FOLDER = getenv("DOWNLOAD_FOLDER", "/data")
CONFIG_FOLDER = getenv("CONFIG_FOLDER", "/config")
DL_FOLDER = BASE_FOLDER

# Telegram login info
BOT_TOKEN = getenv("BOT_TOKEN")
PHONE_NUMBER = getenv("PHONE_NUMBER")
TAPI_ID = int(getenv("TELEGRAM_API_ID", ""))
TAPI_HASH = getenv("TELEGRAM_API_HASH")

for f in [DL_FOLDER, CONFIG_FOLDER]:
    try:
        mkdir(f)
    except FileExistsError:
        pass
    except:
        logging.error(f"Failed to create {f} folder!")
        exit(1)

app = Client(
    "TDownloader-bot",
    TAPI_ID,
    TAPI_HASH,
    bot_token=BOT_TOKEN,
    workdir=CONFIG_FOLDER,
    max_concurrent_transmissions=MAX_SIMULTANEOUS_TRANSMISSIONS,
)

user = None
if PHONE_NUMBER:
    user = Client(
        "TDownloader-user",
        TAPI_ID,
        TAPI_HASH,
        phone_number=PHONE_NUMBER,
        workdir=CONFIG_FOLDER,
        no_updates=True,
        max_concurrent_transmissions=MAX_SIMULTANEOUS_TRANSMISSIONS,
    )
