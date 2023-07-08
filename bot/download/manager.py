from asyncio import create_task, sleep
from textwrap import dedent
from time import ctime, time
from typing import List

from pyrogram.enums import ParseMode
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup)

from .. import BASE_FOLDER, app, folder
from ..util import humanReadable
from .types import Download

downloads: List[Download] = []
running: int = 0
# List of downloads to stop
stop: List[int] = []


async def run():
    global running
    while True:
        for download in downloads:
            if running == 3:
                break
            create_task(downloadFile(download))
            running += 1
            downloads.remove(download)
        try:
            await sleep(1)
        except:
            break


async def downloadFile(download: Download):
    global running
    await download.progress_message.edit(
        text=f"Downloading __{download.filename}__...",
        parse_mode=ParseMode.MARKDOWN
    )
    download.started = time()
    result = await app.download_media(
        message=download.from_message,
        file_name=BASE_FOLDER+'/'+download.filename,
        progress=progress,
        progress_args=tuple([download])
    )
    if isinstance(result, str):
        speed = humanReadable(
            download.size / (download.last_call - download.started))
        await download.progress_message.edit(
            dedent(f"""
                File `{download.filename}` downloaded.

                Downloaded started at __{ctime(download.started)}__ and finished at __{ctime(download.last_call)}__
                It's an average speed of __{speed}/s__
            """),
            parse_mode=ParseMode.MARKDOWN
        )
    running -= 1


async def progress(received: int, total: int, download: Download):
    # This function is called every time that 1MB is downloaded
    if download.id in stop:
        await download.progress_message.edit(
            text=f"Download of `{download.filename}` stopped!",
            parse_mode=ParseMode.MARKDOWN
        )
        await app.stop_transmission()
        stop.remove(download.id)
        return
    # Only update download progress if the last update is 1 second old
    # : This avoid flood on networks that is more than 1MB/s speed
    now = time()
    if download.last_update != 0 and (time() - download.last_update) < 1:
        download.size = total
        download.last_call = now
        return
    percent = received / total * 100
    if download.last_call == 0:
        download.last_call = now - 1
    speed = (1024**2) / (now - download.last_call)
    avg_speed = received / (now - download.started)
    await download.progress_message.edit(
        text=dedent(f'''
            Downloading: `{download.filename}`

            Downloaded __{humanReadable(received)}__ of __{humanReadable(total)}__ (__{percent:.2f}%__)
            __{humanReadable(speed)}/s__ | __{humanReadable(avg_speed)}/s__ avg speed
        '''),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Stop", callback_data=f"stop {download.id}")
        ]])
    )
    download.last_update = now
    download.last_call = now


async def stopDownload(_, callback: CallbackQuery):
    id = int(callback.data.split()[-1])
    stop.append(id)
    await callback.answer("Stopping...")
