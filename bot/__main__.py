from pyrogram.filters import command, document, media
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
from pyrogram.handlers.message_handler import MessageHandler

from pyrogram import idle
from . import app, commands, download
from threading import Thread

app.add_handler(MessageHandler(commands.start, command('start')))
app.add_handler(MessageHandler(commands.botHelp, command('help')))
app.add_handler(MessageHandler(commands.usage, command('usage')))
app.add_handler(MessageHandler(download.handler.addFile, document | media))
app.add_handler(CallbackQueryHandler(download.manager.stopDownload))

app.start()
t = Thread(target=download.manager.run)
t.start()
idle()
t.join()
app.stop()