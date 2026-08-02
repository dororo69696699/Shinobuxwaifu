# ==========================================
# Extended Ping Command
# ==========================================

"""
Extended ping command with additional statistics.
"""

import time
import psutil
import platform
from typing import Optional

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

from app.core.config import Config
from app.filters.admin import AdminOrVIPFilter

logger = logging.getLogger(__name__)

router = Router(name="ping_extended")


@router.message(Command("ping"), AdminOrVIPFilter())
async def ping_extended(
    message: Message,
    bot: Bot,
    config: Config,
) -> None:
    """
    Handle /ping command with extended statistics.
    
    Args:
        message: Incoming message
        bot: Bot instance
        config: Bot configuration
    """
    start_time = time.perf_counter()
    
    # Send initial message
    sent_message = await message.reply("🏓 Pong! Calculating...")
    
    # Calculate metrics
    bot_info = await bot.get_me()
    latency = round((time.perf_counter() - start_time) * 1000, 2)
    
    # System stats
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    
    # Build response
    response = (
        "🏓 <b>Pong! Bot Statistics</b>\n\n"
        f"🤖 <b>Bot:</b> @{bot_info.username}\n"
        f"⚡ <b>Latency:</b> <code>{latency}ms</code>\n"
        f"💻 <b>CPU:</b> <code>{cpu_percent}%</code>\n"
        f"🧠 <b>RAM:</b> <code>{memory.used / 1024**3:.1f}GB / {memory.total / 1024**3:.1f}GB</code>\n"
        f"🖥️ <b>System:</b> <code>{platform.system()} {platform.release()}</code>\n"
        f"🐍 <b>Python:</b> <code>{platform.python_version()}</code>"
    )
    
    await sent_message.edit_text(
        response,
        parse_mode="HTML",
    )
    
    logger.debug(f"Extended ping used by {message.from_user.id}: {latency}ms")
