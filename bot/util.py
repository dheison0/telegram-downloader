from typing import Coroutine

from pyrogram import Client
from pyrogram.types import Message

from . import ADMINS

KIB = 1024
MIB = 1024 * KIB
GIB = 1024 * MIB


def humanReadable(size: int) -> str:
    symbol, divider = "B", 1
    if size >= GIB:
        symbol, divider = "GiB", GIB
    elif size >= MIB:
        symbol, divider = "MiB", MIB
    elif size >= KIB:
        symbol, divider = "KiB", KIB
    readableSize = size / divider
    return f"{readableSize:.1f} {symbol}"


def checkAdmins(func: Coroutine) -> Coroutine:
    async def wrapper(app: Client, message: Message):
        if (f"@{message.chat.username}" not in ADMINS) \
                and (str(message.chat.id) not in ADMINS):
            await message.reply("You aren't my admin :)")
            return
        return await func(app, message)
    return wrapper
