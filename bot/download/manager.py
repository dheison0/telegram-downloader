import logging
from asyncio import create_task, sleep
from textwrap import dedent
from time import ctime, time
from typing import List

from pyrogram.client import Client
from pyrogram.enums import ParseMode
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from .. import BASE_FOLDER, MAX_SIMULTANEOUS_TRANSMISSIONS
from ..util import humanReadableSize, humanReadableTime
from .types import Download

downloads: List[Download] = []
running: int = 0
# List of downloads to stop
stop: List[int] = []


async def run():
    global running
    while True:
        for download in downloads:
            if running == MAX_SIMULTANEOUS_TRANSMISSIONS:
                break
            create_task(downloadFile(download))
            logging.info(f"New download initialized: {download.filename}")
            running += 1
            downloads.remove(download)
        try:
            await sleep(1)
        except:
            break


async def downloadFile(download: Download):
    global running
    await download.progress_message.edit(
        text=f"Starting download...",
        parse_mode=ParseMode.MARKDOWN,
    )
    download.started = time()
    result = await download.client.download_media(
        message=download.from_message,
        file_name=BASE_FOLDER + "/" + download.filename,
        progress=createProgress(download.client),
        progress_args=tuple([download]),
    )
    if isinstance(result, str):
        seconds_took = download.last_update - download.started
        speed = humanReadableSize(download.size / seconds_took)
        time_took = humanReadableTime(int(seconds_took))
        await download.progress_message.edit(
            dedent(f"""
                File `{download.filename}` downloaded.
                Download of {humanReadableSize(download.size)} complete in {time_took}, it's an average speed of __{speed}/s__
            """),
            parse_mode=ParseMode.MARKDOWN,
        )
    running -= 1


def createProgress(client: Client):
    async def progress(received: int, total: int, download: Download):
        # This function is called every time that 1MB is downloaded
        if download.id in stop:
            await download.progress_message.edit(
                text=f"Download of `{download.filename}` stopped!",
                parse_mode=ParseMode.MARKDOWN,
            )
            stop.remove(download.id)
            client.stop_transmission()
            return
        # Only update download progress if the last update is 1 second old
        # : This avoid flood on networks that is more than 1MB/s speed
        now = time()
        if download.last_update != 0 and (time() - download.last_update) < running:
            # Do not update message time from last_update is less than running download count
            return
        download.last_update = now
        percent = received / total * 100
        avg_speed = received / (now - download.started)
        tte = int((total - received) / avg_speed)
        await download.progress_message.edit(
            text=dedent(f"""
            `{download.filename}`:
            __{humanReadableSize(received)}/{humanReadableSize(total)} {percent:0.2f}%
            {humanReadableSize(avg_speed)}/s {humanReadableTime(tte)} till complete__
            """),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Stop", callback_data=f"stop {download.id}")]]
            ),
        )
        download.last_update = now
        download.size = total

    return progress


async def stopDownload(_, callback: CallbackQuery):
    id = int(callback.data.split()[-1])
    stop.append(id)
    await callback.answer("Stopping...")
