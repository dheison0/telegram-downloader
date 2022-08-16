from email.message import Message
from . import app, commands, downloader
from pyrogram.filters import command, document, media
from pyrogram.handlers.message_handler import MessageHandler

app.add_handler(MessageHandler(commands.start, command('start')))
app.add_handler(MessageHandler(commands.botHelp, command('help')))
app.add_handler(MessageHandler(commands.usage, command('usage')))
app.add_handler(MessageHandler(downloader.download, document | media))

app.run()