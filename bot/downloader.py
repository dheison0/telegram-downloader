from dataclasses import dataclass
from random import choices, randint
from string import ascii_letters, digits
from time import time
from typing import Dict, List

from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from . import DL_FOLDER, util


@dataclass
class Download:
    id: int
    filename: str
    progress_message: Message
    started: float
    last_update: float
    last_call: float = 0


# List of running downloads
downloading: Dict[int, Download] = {}
# List of downloads to stop
stop: List[int] = []


async def download(app: Client, msg: Message):
    caption = msg.caption or ""
    if caption[:1] == '>':
        filename = caption[2:]
    else:
        try:
            media = getattr(msg, msg.media.value)
            filename = media.file_name
        except AttributeError:
            filename = ''.join(choices(ascii_letters+digits, k=12))
    reply = await msg.reply("Downloading...")
    id = randint(1e9, 1e10-1)
    downloading[id] = Download(id, filename, reply, time(), 0)
    r = await app.download_media(
        message=msg,
        file_name=DL_FOLDER+'/'+filename,
        progress=progress,
        progress_args=(app, downloading[id])
    )
    downloading.pop(id)
    if r is not None:
        await app.edit_message_text(
            chat_id=reply.chat.id,
            message_id=reply.id,
            text=f"File saved as `{filename}`",
            parse_mode=ParseMode.MARKDOWN
        )


async def progress(received: int, total: int, app: Client, download: Download):
    # This function is called every time that 1MB is downloaded
    if download.id in stop:
        await app.edit_message_text(
            chat_id=download.progress_message.chat.id,
            message_id=download.progress_message.id,
            text=f"Download of __{download.filename}__ stopped!",
            parse_mode=ParseMode.MARKDOWN
        )
        app.stop_transmission()
        stop.remove(download.id)
        downloading.pop(download.id)
        return
    # Only update download progress if the last update is 1 second old
    # : This avoid flood on networks that is more than 1MB/s speed
    now = time()
    if download.last_update != 0 and (time() - download.last_update) < 1:
        download.last_call = now
        return
    percent = received / total * 100
    if download.last_call == 0:
        download.last_call = now - 1
    speed = (1024**2) / (now - download.last_call)
    avg_speed = received / (now - download.started)
    text = f"Downloading: __{download.filename}__\n\n"
    text += f"__{util.humanReadable(received)} of {util.humanReadable(total)} ({percent:.2f}%)\n"
    text += f"{util.humanReadable(speed)}/s or {util.humanReadable(avg_speed)}/s average since start__"
    await app.edit_message_text(
        chat_id=download.progress_message.chat.id,
        message_id=download.progress_message.id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Stop", callback_data=f"stop {download.id}")
        ]])
    )
    download.last_update = time()
    download.last_call = time()


async def stopDownload(_, callback: CallbackQuery):
    id = int(callback.data.split()[-1])
    stop.append(id)
    await callback.answer("Stopping...")
