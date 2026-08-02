# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Ctime Command - Set message count threshold for groups
"""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from config import OWNER_ID
from database.models import get_collection

router = Router(name="ctime")


@router.message(Command("ctime"))
async def ctime_command(message: Message) -> None:
    """Handle /ctime command."""
    chat_id = str(message.chat.id)
    user_id = message.from_user.id
    args = message.text.split()
    
    # Only admins or owner can use
    # For now, allow anyone
    if len(args) != 2:
        await message.reply("Usage: `/ctime <number>`", parse_mode=ParseMode.HTML)
        return
    
    try:
        ctime = int(args[1])
    except ValueError:
        await message.reply("Please provide a valid number.", parse_mode=ParseMode.HTML)
        return
    
    if ctime < 1 or ctime > 200:
        await message.reply("Ctime must be between 1 and 200.", parse_mode=ParseMode.HTML)
        return
    
    groups_collection = get_collection("group_settings")
    await groups_collection.update_one(
        {"group_id": chat_id},
        {"$set": {"ctime": ctime}},
        upsert=True
    )
    
    await message.reply(f"✅ Message count threshold set to {ctime} for this group.")
