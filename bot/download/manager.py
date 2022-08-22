from time import time, sleep
from typing import List

from pyrogram.enums import ParseMode
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup)

from .. import util, app, BASE_FOLDER
from .type import Download
from threading import Thread

downloads: List[Download] = []
running: int = 0
# List of downloads to stop
stop: List[int] = []


def run():
    global running
    while True:
        for download in downloads:
            if running == 3:
                break
            Thread(target=downloadFile, args=(download,)).start()
            running += 1
            downloads.remove(download)
        sleep(1)


def downloadFile(d: Download):
    global running
    d.progress_message = d.from_message.reply(
        text=f"Downloading __{d.filename}__...",
        parse_mode=ParseMode.MARKDOWN
    )
    d.started = time()
    r = app.download_media(
        message=d.from_message,
        file_name=BASE_FOLDER+'/'+d.filename,
        progress=progress,
        progress_args=tuple([d])
    )
    if r:
        text = f"File __{d.filename}__ downloaded."
    else:
        text = f"Download of __{d.filename}__ stopped!"
    app.edit_message_text(
        chat_id=d.progress_message.chat.id,
        message_id=d.progress_message.id,
        text=text,
        parse_mode=ParseMode.MARKDOWN
    )
    running -= 1


async def progress(received: int, total: int, download: Download):
    # This function is called every time that 1MB is downloaded
    if download.id in stop:
        await app.edit_message_text(
            chat_id=download.progress_message.chat.id,
            message_id=download.progress_message.id,
            text=f"Download of __{download.filename}__ stopped!",
            parse_mode=ParseMode.MARKDOWN
        )
        await app.stop_transmission()
        stop.remove(download.id)
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
