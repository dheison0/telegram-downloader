import logging
from os import getenv, mkdir

from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

if getenv('DEBUG') == "1":
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.ERROR)

ADMINS = getenv('ADMINS').split()
BASE_FOLDER = getenv('DOWNLOAD_FOLDER', '/data')
DL_FOLDER = BASE_FOLDER

try:
    mkdir(DL_FOLDER)
except FileExistsError:
    pass
except:
    logging.error('Failed to create data storage path!')
    exit(1)

app = Client(
    name='TDownloader',
    api_id=int(getenv('TELEGRAM_API_ID')),
    api_hash=getenv('TELEGRAM_API_HASH'),
    bot_token=getenv('BOT_TOKEN')
)
