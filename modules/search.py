# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Search Command - /sips to search characters
"""

import re

from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_collection
from assets.rarities import RARITY_MAP

router = Router(name="search")


@router.message(Command("sips"))
async def search_command(message: Message) -> None:
    """Handle /sips command."""
    args = message.text.split()
    if len(args) < 2:
        await message.reply(
            "🌸 Please tell me which spirit you're seeking!\nUsage: `/sips [character name]`",
            parse_mode=ParseMode.HTML
        )
        return
    
    query = " ".join(args[1:]).strip()
    await handle_search(message, query, page=1)


async def handle_search(message, query, page=1, is_callback=False):
    """Handle search with pagination."""
    characters_collection = get_collection("characters")
    per_page = 10
    skip = (page - 1) * per_page
    
    regex = re.compile(query, re.IGNORECASE)
    total = await characters_collection.count_documents({"name": regex})
    
    if total == 0:
        text = "🌸 No spirits match that name, dear. Would you like to try another?"
        if is_callback:
            await message.edit_text(text, parse_mode=ParseMode.HTML)
        else:
            await message.reply(text, parse_mode=ParseMode.HTML)
        return
    
    characters = await characters_collection.find({"name": regex}).skip(skip).limit(per_page).to_list(length=per_page)
    
    response = f"🌸 <b>Spirits Found:</b> {total}\n\n"
    for idx, char in enumerate(characters, start=1 + skip):
        response += (
            f"◈⌠{char.get('rarity', '⭐')}⌡ <b>{idx}</b> {char.get('name', 'Unknown')}\n"
            f"⛩️ Anime: {char.get('anime', 'Unknown')}\n"
            f"🆔 ID: <code>{char.get('id', '')}</code>\n\n"
        )
    
    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"sips:{query}:{page - 1}"))
    if skip + per_page < total:
        buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"sips:{query}:{page + 1}"))
    
    reply_markup = InlineKeyboardMarkup([buttons]) if buttons else None
    
    if is_callback:
        await message.edit_text(response, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        await message.reply(response, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
