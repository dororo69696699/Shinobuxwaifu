
# ==========================================

"""
Main entry point for the Waifu Bot.
Initializes all components, validates permissions, and starts the bot.
"""

import asyncio
import sys
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from app.core.config import Config
from app.core.logging import setup_logging, get_logger
from app.database.manager import DatabaseManager
from app.services.validator import PermissionValidator
from app.handlers import register_all_handlers
from app.middleware import register_all_middleware
from app.callbacks import register_all_callbacks

logger = get_logger("main")


async def setup_bot_commands(bot: Bot) -> None:
    """
    Set up bot commands for the menu.
    
    Args:
        bot: Bot instance
    """
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Get help"),
        BotCommand(command="profile", description="View your profile"),
        BotCommand(command="shop", description="Visit the shop"),
        BotCommand(command="gacha", description="Roll for waifus"),
        BotCommand(command="daily", description="Claim daily reward"),
        BotCommand(command="waifu", description="Manage your waifus"),
        BotCommand(command="inventory", description="View your inventory"),
        BotCommand(command="marry", description="Marry your waifu"),
        BotCommand(command="divorce", description="Divorce your waifu"),
    ]
    
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    logger.info("✅ Bot commands registered")


async def initialize_bot(config: Config) -> None:
    """
    Initialize bot components asynchronously.
    
    Args:
        config: Configuration instance
    
    Raises:
        Exception: If initialization fails
    """
    logger.info("🦋 Initializing WaifuBot...")
    
    # Initialize database
    logger.info("🔄 Initializing database...")
    db_manager = DatabaseManager(config)
    await db_manager.initialize()
    await db_manager.create_indexes()
    logger.info("✅ Database initialized")
    
    # Validate channel permissions
    logger.info("🔄 Validating channel permissions...")
    validator = PermissionValidator(config)
    
    # Validate force join channel
    force_join_link = await validator.validate_force_join_channel()
    config.FORCE_JOIN_LINK = force_join_link
    logger.info(f"✅ Force join channel verified: {force_join_link}")
    
    # Validate logging channel
    await validator.validate_logging_channel()
    logger.info("✅ Logging channel verified")
    
    # Send startup notification
    await validator.send_startup_notification()
    logger.info("✅ Startup notification sent")
    
    logger.info("✅ Bot initialization complete")


async def main() -> None:
    """Main entry point for the bot."""
    try:
        # Load configuration
        config = Config()
        
        # Setup logging
        setup_logging(config)
        logger.info("🚀 Starting WaifuBot v2.0...")
        
        # Initialize bot
        await initialize_bot(config)
        
        # Create bot and dispatcher instances
        bot = Bot(token=config.BOT_TOKEN)
        dp = Dispatcher()
        
        # Register middleware
        register_all_middleware(dp, config)
        logger.info("✅ Middleware registered")
        
        # Register handlers
        register_all_handlers(dp)
        logger.info("✅ Handlers registered")
        
        # Register callbacks
        register_all_callbacks(dp)
        logger.info("✅ Callbacks registered")
        
        # Setup bot commands
        await setup_bot_commands(bot)
        
        # Store bot instance in config for global access
        config.bot = bot
        config.dispatcher = dp
        
        logger.info(
            "╔═══════════════════════════════════════╗\n"
            "║  🦋 WaifuBot is now running!          ║\n"
            "║  Made with ❤️ by Team Egoist          ║\n"
            "║  Press Ctrl+C to stop                 ║\n"
            "╚═══════════════════════════════════════╝"
        )
        
        # Start polling
        try:
            await dp.start_polling(
                bot,
                drop_pending_updates=True,
                allowed_updates=["message", "callback_query", "inline_query"]
            )
        except (KeyboardInterrupt, SystemExit):
            logger.info("🛑 Bot stopped by user")
        finally:
            await shutdown_cleanup(bot, config)
            
    except Exception as e:
        logger.critical(f"❌ Fatal error during startup: {e}", exc_info=True)
        sys.exit(1)


async def shutdown_cleanup(bot: Bot, config: Config) -> None:
    """
    Perform graceful shutdown cleanup.
    
    Args:
        bot: Bot instance
        config: Configuration instance
    """
    logger.info("🔄 Shutting down gracefully...")
    
    try:
        # Close database connections
        if hasattr(config, 'db_manager'):
            await config.db_manager.close()
            logger.info("✅ Database connections closed")
        
        # Close bot session
        await bot.session.close()
        logger.info("✅ Bot session closed")
        
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")
    
    logger.info("👋 Goodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"❌ Unhandled exception: {e}", exc_info=True)
        sys.exit(1)
