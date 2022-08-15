from . import app, commands
from pyrogram.filters import command, document
from pyrogram.handlers.message_handler import MessageHandler

app.add_handler(MessageHandler(commands.start, command('start')))
app.add_handler(MessageHandler(commands.usage, command('usage')))

app.run()