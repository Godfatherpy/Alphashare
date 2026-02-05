from pyrogram import Client, idle
from web import start_webserver, ping_server
from database import Database
import config
import asyncio
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ReferralBot(Client):
    def __init__(self):
        super().__init__(
            name="ReferralBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins=dict(root="handlers")
        )
        self.db = Database()
        logger.info("Bot Initialized!")

    async def start(self):
        await super().start()
        me = await self.get_me()
        logger.info(f"Bot Started as {me.first_name} (@{me.username})")

    async def stop(self, *args):
        await super().stop()
        logger.info("Bot Stopped. Bye!")

async def main():
    bot = ReferralBot()
    
    try:
        logger.info("Starting Bot...")
        await bot.start()

        if config.WEB_SERVER:
            logger.info("Starting Web Server...")
            asyncio.create_task(start_webserver())
            if config.PING_URL:
                asyncio.create_task(ping_server(config.PING_URL, config.PING_TIME))
            
        await idle()
    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
    finally:
        await bot.stop()

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot Stopped by User!")
    except Exception as e:
        logger.critical(f"CRITICAL ERROR: {str(e)}")
