# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Broadcast Command - Send message to all users
"""

import asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from filters.admin import AdminOrVIPFilter
from database.models import get_collection

router = Router(name="broadcast")


@router.message(Command(["bcast", "broadcast"]), AdminOrVIPFilter())
async def broadcast_command(message: Message) -> None:
    """Handle /broadcast command."""
    if not message.reply_to_message:
        await message.reply(
            "📢 <b>Broadcast</b>\n\nPlease reply to a message to broadcast it.",
            parse_mode=ParseMode.HTML
        )
        return
    
    progress = await message.reply(
        "📢 Starting broadcast...",
        parse_mode=ParseMode.HTML
    )
    
    users_collection = get_collection("users")
    user_count = await users_collection.count_documents({})
    
    success = 0
    fail = 0
    
    async for user in users_collection.find({}):
        user_id = user.get('id')
        if not user_id:
            continue
        
        try:
            await message.reply_to_message.forward(user_id)
            success += 1
        except Exception:
            fail += 1
        
        if (success + fail) % 10 == 0:
            await progress.edit_text(
                f"📢 <b>Broadcast Progress</b>\n\n"
                f"✅ Sent: {success}\n"
                f"❌ Failed: {fail}\n"
                f"📊 Progress: {success + fail}/{user_count}",
                parse_mode=ParseMode.HTML
            )
    
    await progress.edit_text(
        f"✅ <b>Broadcast Complete</b>\n\n"
        f"👤 Users: {success}\n"
        f"❌ Failed: {fail}",
        parse_mode=ParseMode.HTML
    )
