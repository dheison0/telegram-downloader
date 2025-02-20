import asyncio
import logging

from pyrogram import idle

from . import app, commands, download, user


async def main():
    logging.info("Registering commands...")
    commands.register(app)
    logging.info("Starting bot...")
    await app.start()
    if user:
        logging.info("Starting normal user")
        await user.start()
    logging.info("Starting download manager...")
    manager = asyncio.create_task(download.manager.run())
    me = await app.get_me()
    logging.info(f"Bot started! I'm @{me.username}")
    await idle()
    logging.info("Stopping download manager...")
    manager.cancel()
    logging.info("Stopping bot...")
    await app.stop()
    if user:
        logging.info("Stopping user...")
        await user.stop()
    logging.info("All systems stopped!")
    return 0


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main())
