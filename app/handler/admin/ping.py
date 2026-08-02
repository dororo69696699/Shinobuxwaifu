# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# Rewritten with Clean Architecture
# ==========================================

"""
Ping Command Handler

Provides bot response time measurement for VIP and admin users.
"""

import logging
import time
from typing import Optional

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.core.config import Config
from app.services.permissions import PermissionService
from app.filters.admin import AdminOrVIPFilter

logger = logging.getLogger(__name__)

router = Router(name="ping")


@router.message(Command("ping"), AdminOrVIPFilter())
async def ping_command(
    message: Message,
    bot: Bot,
    config: Config,
) -> None:
    """
    Handle /ping command - measures bot response time.
    
    Args:
        message: Incoming message
        bot: Bot instance
        config: Bot configuration
    """
    # Measure start time
    start_time = time.perf_counter()
    
    # Send initial pong message
    sent_message = await message.reply("🏓 Pong!")
    
    # Calculate elapsed time
    end_time = time.perf_counter()
    elapsed_ms = round((end_time - start_time) * 1000, 2)
    
    # Edit message with ping time
    await sent_message.edit_text(
        f"🏓 Pong! <code>{elapsed_ms}ms</code>",
        parse_mode="HTML",
    )
    
    logger.debug(f"Ping command used by {message.from_user.id}: {elapsed_ms}ms")


@router.message(Command("ping"))
async def ping_denied(
    message: Message,
) -> None:
    """
    Handle /ping command for unauthorized users.
    
    Args:
        message: Incoming message
    """
    await message.reply(
        "🚫 <b>Access Denied</b>\n\n"
        "Only <b>VIP</b> users or the <b>Owner</b> can use this command.",
        parse_mode="HTML",
)
