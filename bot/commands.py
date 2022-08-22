import textwrap

from pyrogram.enums import ParseMode
from pyrogram.types import Message

from . import DL_FOLDER, sysinfo, BASE_FOLDER
from . import folder
from os import mkdir


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
        f"I'm running on a system with __{u.capacity}__ of storage and it's using __{u.used}__, this is __{u.percent}__ of the capacity, so it has __{u.free}__ free",
        parse_mode=ParseMode.MARKDOWN
    )


async def botHelp(_, msg: Message):
    await msg.reply("// TODO")


async def useFolder(_, msg: Message):
    newFolder = ''.join(msg.text.split()[1:])
    try:
        mkdir(BASE_FOLDER + '/' + newFolder)
    except FileExistsError:
        pass
    except Exception as err:
        await msg.reply(f"Failed to open folder: {err}")
        return
    folder.set(newFolder)
    await msg.reply("Ok, send me files now and I will put it on this folder.")


async def leaveFolder(_, msg: Message):
    folder.set('.')
    await msg.reply("I'm in the root folder again.")
