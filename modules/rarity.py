# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Rarity Command - Show character counts by rarity
"""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_collection
from assets.rarities import RARITY_MAP

router = Router(name="rarity")


@router.message(Command("rarity"))
async def rarity_command(message: Message) -> None:
    """Handle /rarity command."""
    characters_collection = get_collection("characters")
    
    text = "🌸 <b>Wisteria Rarity Ledger</b>\n"
    text += "━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    total = 0
    
    for rarity_no in sorted(RARITY_MAP.keys()):
        rarity_name = RARITY_MAP[rarity_no]
        count = await characters_collection.count_documents({"rarity_number": rarity_no})
        total += count
        text += f"{rarity_name}\n   ↬ {count} souls\n\n"
    
    text += "━━━━━━━━━━━━━━━━━━━━━\n"
    text += f"🦋 <b>Total Souls</b> ↬ {total}\n\n"
    text += "<i>\"Every butterfly has its place beneath the wisteria.\"</i>"
    
    await message.reply(text, parse_mode=ParseMode.HTML)
