
# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# Rewritten with Clean Architecture
# ==========================================

"""
Start Command Handler

Handles the /start command for private and group chats with:
- Custom welcome messages
- User registration
- Media display
- Navigation buttons
"""

import logging
import random
import time
from typing import Optional, Tuple, List

from aiogram import Router, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatType

from app.core.config import Config
from app.database.repositories.user import UserRepository
from app.database.models.user import User
from app.filters.chat_type import ChatTypeFilter
from app.services.uptime import UptimeService
from app.keyboards.start import (
    get_private_start_keyboard,
    get_group_start_keyboard,
    get_help_keyboard,
    get_back_keyboard,
)

logger = logging.getLogger(__name__)

router = Router(name="start")


@router.message(CommandStart(), ChatTypeFilter(ChatType.PRIVATE))
async def start_private(
    message: Message,
    bot: Bot,
    config: Config,
    user_repo: UserRepository,
    uptime_service: UptimeService,
) -> None:
    """
    Handle /start command in private chats.
    
    Args:
        message: Incoming message
        bot: Bot instance
        config: Bot configuration
        user_repo: User repository
        uptime_service: Uptime service
    """
    user = message.from_user
    if not user:
        return
    
    # Register user in database
    await _register_user(user, user_repo)
    
    # Log startup
    await _log_user_start(bot, config, user)
    
    # Generate response
    caption, keyboard = await _generate_private_start_message(
        bot, config, uptime_service
    )
    
    # Send with random media
    await _send_media(message, caption, keyboard)
    
    logger.info(f"User {user.id} (@{user.username}) started bot in private")


@router.message(CommandStart(), ChatTypeFilter(ChatType.GROUP, ChatType.SUPERGROUP))
async def start_group(
    message: Message,
    bot: Bot,
    config: Config,
) -> None:
    """
    Handle /start command in groups.
    
    Args:
        message: Incoming message
        bot: Bot instance
        config: Bot configuration
    """
    # Generate response
    caption, keyboard = await _generate_group_start_message(bot, config)
    
    # Send with random media
    await _send_media(message, caption, keyboard)
    
    chat_id = message.chat.id
    logger.info(f"Start command used in group {chat_id}")


# ===== Helper Functions =====

async def _register_user(user, user_repo: UserRepository) -> None:
    """
    Register a user in the database if they don't exist.
    
    Args:
        user: Telegram user
        user_repo: User repository
    """
    existing = await user_repo.get_by_id(user.id)
    if not existing:
        new_user = User(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            start_time=time.time(),
        )
        await user_repo.create(new_user)
        logger.info(f"New user registered: {user.id} (@{user.username})")


async def _log_user_start(bot: Bot, config: Config, user) -> None:
    """
    Log user start to the logging channel.
    
    Args:
        bot: Bot instance
        config: Bot configuration
        user: Telegram user
    """
    try:
        mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        username = f"@{user.username}" if user.username else "No username"
        
        text = (
            f"🦋 {mention} started the bot!\n\n"
            f"<b>User ID:</b> <code>{user.id}</code>\n"
            f"<b>Username:</b> {username}"
        )
        
        await bot.send_message(
            chat_id=config.get_logging_target(),
            text=text,
            parse_mode="HTML",
        )
    except Exception as e:
        logger.error(f"Failed to log user start: {e}")


async def _send_media(
    message: Message,
    caption: str,
    keyboard: InlineKeyboardMarkup,
) -> None:
    """
    Send a message with random media from the configured list.
    
    Args:
        message: Message to reply to
        caption: Caption text
        keyboard: Inline keyboard
    """
    from app.core.config import get_config
    config = get_config()
    
    # Select random media
    media = random.choice(config.START_MEDIA)
    
    try:
        if any(media.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp']):
            await message.reply_photo(
                photo=media,
                caption=caption,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
        elif media.lower().endswith('.gif'):
            await message.reply_animation(
                animation=media,
                caption=caption,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
        else:
            await message.reply_video(
                video=media,
                caption=caption,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
    except Exception as e:
        logger.error(f"Failed to send media: {e}")
        # Fallback to text only
        await message.reply(
            text=caption,
            reply_markup=keyboard,
            parse_mode="HTML",
        )


async def _generate_private_start_message(
    bot: Bot,
    config: Config,
    uptime_service: UptimeService,
) -> Tuple[str, InlineKeyboardMarkup]:
    """
    Generate the private start message and keyboard.
    
    Args:
        bot: Bot instance
        config: Bot configuration
        uptime_service: Uptime service
        
    Returns:
        Tuple of (caption, keyboard)
    """
    bot_user = await bot.get_me()
    bot_name = bot_user.first_name
    uptime = uptime_service.get_uptime_string()
    
    caption = (
        f"🌸 <b>Welcome to {bot_name}!</b> 🌸\n\n"
        f"<i>I'm your waifu companion. I'll help you discover and collect "
        f"anime characters from various worlds. Don't worry, the fresh "
        f"grass is safe from me.</i>\n\n"
        f"<blockquote>\n"
        f"┈┈┈┈┈┈┈▣▢▣┈┈┈┈┈┈┈\n"
        f"✦ <b>Mission:</b> I travel around spaces and track "
        f"down hidden demons in your chats.\n"
        f"✦ <b>Training:</b> Add me to your group and use /help to read "
        f"my training manual.\n"
        f"┈┈┈┈┈┈┈▣▢▣┈┈┈┈┈┈┈\n"
        f"⚡ <b>Ping:</b> <code>~{uptime_service.get_ping()}ms</code>\n"
        f"⏳ <b>Uptime:</b> <code>{uptime}</code>\n"
        f"</blockquote>"
    )
    
    keyboard = get_private_start_keyboard(bot_user.username)
    return caption, keyboard


async def _generate_group_start_message(
    bot: Bot,
    config: Config,
) -> Tuple[str, InlineKeyboardMarkup]:
    """
    Generate the group start message and keyboard.
    
    Args:
        bot: Bot instance
        config: Bot configuration
        
    Returns:
        Tuple of (caption, keyboard)
    """
    bot_user = await bot.get_me()
    
    caption = (
        f"🦋 <i>Hello, hello... I am</i> <b>{bot_user.first_name}</b> 🌸\n\n"
        f"<blockquote>\n"
        f"I am currently monitoring this chat to detect and collect "
        f"anime characters through messages.\n\n"
        f"Use /help to access my special media and combat manuals!\n"
        f"</blockquote>"
    )
    
    keyboard = get_group_start_keyboard()
    return caption, keyboard
