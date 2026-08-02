# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Message Counter Handler - Auto-send characters based on message count
"""

from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode

from database.models import get_collection

router = Router(name="message_counter")


@router.message()
async def message_counter(message: Message) -> None:
    """Count messages and trigger character spawns."""
    # Skip commands
    if message.text and message.text.startswith('/'):
        return
    
    chat_id = str(message.chat.id)
    
    groups_collection = get_collection("group_settings")
    settings = await groups_collection.find_one({"group_id": chat_id})
    ctime = settings.get("ctime", 80) if settings else 80
    
    # Simple counter - in production use Redis or database
    # This is a simplified version
    pass
