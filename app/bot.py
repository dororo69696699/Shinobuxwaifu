# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Bot factory module for creating and configuring bot instances.
"""

from typing import Optional, Tuple

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from app.core.config import Config


def create_bot(config: Config) -> Bot:
    """
    Create and configure an Aiogram bot instance.
    
    Args:
        config: Bot configuration
        
    Returns:
        Configured Bot instance
    """
    return Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=False,
        ),
    )


def create_dispatcher(
    config: Config,
    use_redis: bool = False,
    redis_url: Optional[str] = None
) -> Dispatcher:
    """
    Create and configure an Aiogram dispatcher instance.
    
    Args:
        config: Bot configuration
        use_redis: Whether to use Redis for FSM storage
        redis_url: Redis connection URL (required if use_redis is True)
        
    Returns:
        Configured Dispatcher instance
    """
    if use_redis:
        if not redis_url:
            raise ValueError("Redis URL is required when use_redis is True")
        storage = RedisStorage.from_url(redis_url)
    else:
        storage = MemoryStorage()
    
    dp = Dispatcher(storage=storage)
    
    # Set config in dp for easy access in handlers
    dp["config"] = config
    
    return dp


def create_application(config: Config) -> Tuple[Bot, Dispatcher]:
    """
    Create both bot and dispatcher instances.
    
    Args:
        config: Bot configuration
        
    Returns:
        Tuple of (Bot, Dispatcher)
    """
    bot = create_bot(config)
    dp = create_dispatcher(config)
    return bot, dp


# Backward compatibility
async def get_bot() -> Bot:
    """
    Get or create a bot instance.
    This is maintained for backward compatibility.
    """
    from app.core.config import get_config
    config = get_config()
    if config.bot is None:
        config.bot = create_bot(config)
    return config.bot


async def get_dispatcher() -> Dispatcher:
    """
    Get or create a dispatcher instance.
    This is maintained for backward compatibility.
    """
    from app.core.config import get_config
    config = get_config()
    if config.dispatcher is None:
        config.dispatcher = create_dispatcher(config)
    return config.dispatcher
