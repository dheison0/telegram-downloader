from textwrap import dedent

from pyrogram.client import Client
from pyrogram.enums import ParseMode
from pyrogram.filters import command, document, media
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import Message

from . import DL_FOLDER, download, folder, sysinfo
from .util import checkAdmins


def register(app: Client):
    app.add_handler(MessageHandler(start, command('start')))
    app.add_handler(MessageHandler(botHelp, command('help')))
    app.add_handler(MessageHandler(usage, command('usage')))
    app.add_handler(MessageHandler(useFolder, command('use')))
    app.add_handler(MessageHandler(leaveFolder, command('leave')))
    app.add_handler(MessageHandler(download.handler.addFile, document | media))
    app.add_handler(CallbackQueryHandler(download.manager.stopDownload))


@checkAdmins
async def start(_, message: Message):
    await message.reply(dedent("""
        Hello!
        Send me a file and I will download it to my server.
        If you need help send /help
    """))


@checkAdmins
async def botHelp(_, message: Message):
    await message.reply(dedent("""
        My Commands are:

        /usage: Gets the disk usage
        /use: Use a specific folder inside storage
        /leave: Go back to root storage
    """))


@checkAdmins
async def usage(_, message: Message):
    u = sysinfo.diskUsage(DL_FOLDER)
    await message.reply(
        dedent(f"""
            The storage path configured has __{u.capacity}__ of storage"
            Of those, __{u.used}__ is in use, and __{u.free}__ is free
        """),
        parse_mode=ParseMode.MARKDOWN
    )


@checkAdmins
async def useFolder(_, message: Message):
    args = message.text.split()
    userSetPath = ' '.join(args[1:])
    path = userSetPath.replace('../', '').replace('/..', '')
    if userSetPath != path:
        await message.reply(f"Warning: Path is **{path}** not **{' '.join(args[1:])}**")
    folder.set(path)
    await message.reply("Ok, send me files now and I will put it on this folder.")


@checkAdmins
async def leaveFolder(_, message: Message):
    folder.reset()
    await message.reply("I'm in the root folder again :)")


@checkAdmins
async def getFolder(_, message: Message):
    await message.reply(f"I'm on the \"{folder.getPath()}\" folder")
