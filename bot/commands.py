from . import sysinfo, DL_FOLDER
from pyrogram import Client
from pyrogram.types import Message
import textwrap


async def start(_, msg: Message):
    await msg.reply("Hello!\nSend me a file and I will download it to my server.")


async def usage(_, msg: Message):
    u = sysinfo.diskUsage(DL_FOLDER)
    await msg.reply(
        textwrap.dedent(
            f"""
            Used: {u.used} of {u.capacity}({u.percent})
            Free: {u.free}
            """
        )
    )
