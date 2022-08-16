from . import sysinfo, DL_FOLDER
from pyrogram.types import Message
from pyrogram.enums import ParseMode
import textwrap


async def start(_, msg: Message):
    await msg.reply(
        textwrap.dedent(
            """
            Hello!
            Send me a file and I will download it to my server.
            If you need help send /help
            """
        )
    )


async def usage(_, msg: Message):
    u = sysinfo.diskUsage(DL_FOLDER)
    await msg.reply(
        textwrap.dedent(
            f"""
            Used: __{u.used} of {u.capacity}({u.percent})__
            Free: __{u.free}__
            """
        ),
        parse_mode=ParseMode.MARKDOWN
    )


async def botHelp(_, msg: Message):
    pass
