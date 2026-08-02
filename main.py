import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database.manager import init_db
from modules import register_all_modules
from callbacks import register_all_callbacks
from middleware import setup_middleware

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


async def main():
    logger.info("🦋 Starting WaifuBot...")
    
    await init_db()
    logger.info("✅ Database connected")
    
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    
    await setup_middleware(dp)
    register_all_modules(dp)
    register_all_callbacks(dp)
    
    logger.info("✅ Bot ready!")
    
    try:
        await dp.start_polling(bot, drop_pending_updates=True)
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Goodbye!")
        sys.exit(0)
