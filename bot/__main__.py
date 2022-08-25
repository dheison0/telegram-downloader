from threading import Thread

from pyrogram import idle
from pyrogram.filters import command, document, media
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
from pyrogram.handlers.message_handler import MessageHandler

from . import app, commands, download

app.add_handler(MessageHandler(commands.start, command('start')))
app.add_handler(MessageHandler(commands.botHelp, command('help')))
app.add_handler(MessageHandler(commands.usage, command('usage')))
app.add_handler(MessageHandler(commands.useFolder, command('use')))
app.add_handler(MessageHandler(commands.leaveFolder, command('leave')))
app.add_handler(MessageHandler(download.handler.addFile, document | media))
app.add_handler(CallbackQueryHandler(download.manager.stopDownload))

app.start()
t = Thread(target=download.manager.run)
t.start()
idle()
t.join()
app.stop()
