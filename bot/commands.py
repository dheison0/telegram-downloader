from textwrap import dedent

from pyrogram.client import Client
from pyrogram.enums import ParseMode
from pyrogram.filters import command, document, media
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import Message

from . import DL_FOLDER, folder, sysinfo, user
from .download.handler import addFile, addFileFromUser
from .download.manager import stopDownload
from .util import checkAdmins

bot_help = """
You can send files to me and I'll save it to your storage(where bot is hosted), when sending a file you can set caption as "> filename.ext" to rename it

The name of the files to be downloaded has a priority sequence:
  - Name set on message to add file;
  - Caption starting with ">";
  - Original filename provided by telegram;
  - Random name without extension starting with 'File-'.

This bot is capable of stopping downloads, so don't worry if you don't want a file that is being downloaded :)

My commands are:\n\n"""


def register(app: Client):
    addCommand(app, start, "start")
    addCommand(app, botHelp, "help")
    addCommand(app, usage, "usage")
    addCommand(app, useFolder, "use")
    addCommand(app, leaveFolder, "leave")
    addCommand(app, getFolder, "get")
    addCommand(app, addByLink, "add")
    app.add_handler(MessageHandler(checkAdmins(addFile), document | media))
    app.add_handler(CallbackQueryHandler(stopDownload))


def addCommand(app, func, cmd):
    global bot_help
    bot_help += f"/{cmd} - {dedent(func.__doc__ or 'No description').strip()}\n"
    app.add_handler(MessageHandler(checkAdmins(func), command(cmd)))


async def start(_, message: Message):
    """Shows bot start message"""
    await message.reply(
        dedent("""
        Hello!
        Send me a file and I will download it to my server.
        If you need help send /help
    """)
    )


async def botHelp(_, message: Message):
    """Send this message"""
    global bot_help
    await message.reply(bot_help)


async def addByLink(_, message: Message):
    """
    Add a link to download a file from a private channel that doesn't allow forwarding
    First argument is the message link where file is, second is optional and can be used to rename file
    """
    if not user:
        await message.reply("Your bot system isn't configured to access your messages!")
        return
    messageParts = message.text.split()
    if len(messageParts) == 1 or "://" not in messageParts[1]:
        await message.reply("You don't send a link to message!")
        return
    linkParts = messageParts[1].split("/")
    messageID = int(linkParts[-1])
    chatID = int(f"-100{linkParts[-2]}")
    try:
        messages = await user.get_messages(chatID, [messageID])
    except:
        await message.reply("Message not found on normal user!")
        return
    await addFileFromUser(messages[0], message)


async def usage(_, message: Message):
    """
    Lets you know how many storage your device has and how many of it is available
    You can use it to know if your storage has enough available space
    """
    usage = sysinfo.diskUsage(DL_FOLDER)
    await message.reply(
        dedent(f"""
            The storage path configured has __{usage.capacity}__ of storage
            Of those, __{usage.used}__ is in use, and __{usage.free}__ is free.
        """),
        parse_mode=ParseMode.MARKDOWN,
    )


async def useFolder(_, message: Message):
    """
    Set a subfolder for downloading files into it
    This must be used before adding a file to download, so it will be save where you want it
    """
    args = message.text.split()
    userSetPath = " ".join(args[1:]).strip()
    if not userSetPath:
        await message.reply("You haven't told me where I need to put your files!")
        return
    path = userSetPath.replace("../", "").replace("/..", "")
    if userSetPath != path:
        await message.reply(f"Warning: Path is `{path}` not `{' '.join(args[1:])}`")
    folder.set(path)
    await message.reply("Ok, send me files now and I will put it on this folder.")


async def leaveFolder(_, message: Message):
    """Go back to default download folder"""
    folder.reset()
    await message.reply("I'm in the root folder again :)")


async def getFolder(_, message: Message):
    """Get actual download folder"""
    path = folder.getPath()
    await message.reply(f"I'm on the `{path}` folder")
