import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database.manager import close_db, init_db
from middleware import setup_middleware
from modules import register_all_modules
from callbacks import register_all_callbacks
from handlers import register_all_handlers

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


async def main():
    logger.info("🦋 Starting WaifuBot...")

    if not BOT_TOKEN:
        logger.critical("❌ BOT_TOKEN is missing! Please set it in your environment.")
        sys.exit(1)

    # Initialize database connection
    await init_db()
    logger.info("✅ Database connected")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Register middlewares, routers, and handlers
    await setup_middleware(dp)
    register_all_modules(dp)
    register_all_callbacks(dp)
    register_all_handlers(dp)

    logger.info("✅ Bot ready! Starting polling...")

    try:
        await dp.start_polling(bot, drop_pending_updates=True)
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped manually")
    finally:
        await bot.session.close()
        await close_db()
        logger.info("🔒 Connections closed safely")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("👋 Goodbye!")
        sys.exit(0)
