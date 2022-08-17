from pyrogram.filters import command, document, media
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
from pyrogram.handlers.message_handler import MessageHandler

from . import app, commands, downloader

app.add_handler(MessageHandler(commands.start, command('start')))
app.add_handler(MessageHandler(commands.botHelp, command('help')))
app.add_handler(MessageHandler(commands.usage, command('usage')))
app.add_handler(MessageHandler(downloader.download, document | media))
app.add_handler(CallbackQueryHandler(downloader.stopDownload))

app.run()
