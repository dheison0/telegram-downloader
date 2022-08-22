from random import choices, randint
from string import ascii_letters, digits
from time import time

from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message

from .manager import downloads
from .type import Download
from ..import folder


async def addFile(_, msg: Message):
    caption = msg.caption or ""
    filename = folder.get() + '/'
    if caption[:1] == '>':
        filename += caption[2:]
    else:
        try:
            media = getattr(msg, msg.media.value)
            filename += media.file_name
        except AttributeError:
            filename += ''.join(choices(ascii_letters+digits, k=12))
    m = await msg.reply(
        f"File __{filename}__ added to list.",
        parse_mode=ParseMode.MARKDOWN
    )
    downloads.append(Download(
        id=randint(1e9, 1e10-1),
        filename=filename,
        from_message=msg,
        added=time(),
        progress_message=m
    ))
