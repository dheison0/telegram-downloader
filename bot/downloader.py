from . import DL_FOLDER, util
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from time import time
import textwrap, random, string


async def download(app: Client, msg: Message):
    filename = DL_FOLDER + '/'
    caption = msg.caption or ""
    media = getattr(msg, msg.media.value)
    if caption[:1] == '>':
        filename += caption[2:]
    else:
        try:
            filename += media.file_name
        except AttributeError:
            filename += ''.join(random.choices(string.ascii_letters+string.digits, k=12))
    reply = await msg.reply("Downloading...")
    await app.download_media(
        message=msg,
        file_name=filename,
        progress=progress,
        progress_args=(app, reply, filename)
    )


last_time = 0
async def progress(received: int, total: int, app: Client, pmsg: Message, filename: str):
    # This function is called every time that 1MB is downloaded
    global last_time
    if received == total:
        await app.edit_message_text(
            chat_id=pmsg.chat.id,
            message_id=pmsg.id,
            text=f"File saved as `{filename}`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    percent = received / total * 100
    # Get speed based on time to download 1MB
    now = time()
    if last_time == 0:
        last_time = now - 1
    speed = (1024**2) / (now - last_time)
    last_time = now
    await app.edit_message_text(
        chat_id=pmsg.chat.id,
        message_id=pmsg.id,
        text=textwrap.dedent(f"""
            Size: __{util.humanReadable(total)}__
            Downloaded: __{util.humanReadable(received)} ({percent:.2f}%)__
            Speed: __{util.humanReadable(speed)}/s__
        """),
        parse_mode=ParseMode.MARKDOWN
    )
