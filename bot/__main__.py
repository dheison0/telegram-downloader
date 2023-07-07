import asyncio
import logging

from pyrogram import idle

from . import app, commands, download


async def main():
    logging.info("Registering commands...")
    commands.register(app)
    await app.start()
    logging.info("Starting download manager...")
    manager = asyncio.create_task(download.manager.run())
    me = await app.get_me()
    logging.info(f"Bot started! I'm @{me.username}")
    await idle()
    logging.info("Stopping bot...")
    manager.cancel()
    await app.stop()
    logging.info("Bot stopped!")
    return 0

event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main())
