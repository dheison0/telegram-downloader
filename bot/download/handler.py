import os
from random import randint
from time import time

from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message

from .. import folder
from .manager import downloads
from .types import Download


async def addFile(_, message: Message):
    caption = (message.caption or "").strip()
    filename = f'File-{randint(1e9, 1e10-1)}'
    if caption[:1] == '>':
        filename = caption[2:].strip()
    else:
        try:
            media = getattr(message, message.media.value)
            filename = media.file_name
        except AttributeError:
            pass
    file = os.path.join(folder.getPath(), filename)
    realFile = os.path.join(folder.get(), filename)
    if os.path.isfile(realFile):
        return await message.reply(
            text=f"File __{file}__ already exists!",
            quote=True
        )
    progress = await message.reply(
        f"File __{file}__ added to list.",
        quote=True,
        parse_mode=ParseMode.MARKDOWN
    )
    downloads.append(Download(
        id=message.id,
        filename=file,
        from_message=message,
        progress_message=progress
    ))
