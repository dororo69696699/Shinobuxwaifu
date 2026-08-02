# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Harem/Collection Command - View user's character collection
"""

import math
import random
from html import escape
from itertools import groupby

from aiogram import Router, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_user, get_collection
from assets.rarities import RARITY_MAP, RARITY_NAMES
from utils.inline import get_user_collection

router = Router(name="harem")


@router.message(Command(["harem", "collection"]))
async def harem_command(message: Message) -> None:
    """Handle /harem or /collection command."""
    user_id = message.from_user.id
    page = 0
    filter_rarity = None
    
    await display_harem(message, user_id, page, filter_rarity, is_initial=True)


async def display_harem(message, user_id, page, filter_rarity, is_initial=False, callback_query=None):
    """Display user's harem/collection."""
    users_collection = get_collection("users")
    characters_collection = get_collection("characters")
    
    user = await users_collection.find_one({"id": user_id})
    if not user or 'characters' not in user:
        text = "🦋 <i>Ara ara~ You have not collected any souls in your Butterfly Garden yet!</i>"
        if is_initial:
            await message.reply(text, parse_mode=ParseMode.HTML)
        else:
            await callback_query.message.edit_text(text, parse_mode=ParseMode.HTML)
        return
    
    characters = [c for c in user['characters'] if 'id' in c]
    if not characters:
        text = "🦋 <i>Ara ara? I could not find any valid records inside your collection.</i>"
        if is_initial:
            await message.reply(text, parse_mode=ParseMode.HTML)
        else:
            await callback_query.message.edit_text(text, parse_mode=ParseMode.HTML)
        return
    
    # Filter by rarity if specified
    if filter_rarity:
        characters = [c for c in characters if c.get('rarity') == filter_rarity]
        if not characters:
            keyboard = [[InlineKeyboardButton("🦋 Remove Rarity Filter", callback_data=f"remove_filter:{user_id}")]]
            text = f"🦋 No souls under <b>{filter_rarity}</b> in your garden."
            if is_initial:
                await message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
            else:
                await callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
            return
    
    # Sort and group characters
    characters = sorted(characters, key=lambda x: (x.get('anime', ''), x.get('id', '')))
    character_counts = {k: len(list(v)) for k, v in groupby(characters, key=lambda x: x['id'])}
    unique_characters = list({char['id']: char for char in characters}.values())
    
    total_pages = math.ceil(len(unique_characters) / 15)
    if page < 0 or page >= total_pages:
        page = 0
    
    # Build message
    user_first_name = user.get('first_name', 'User')
    harem_message = f"🦋 <b>{escape(user_first_name)}'s Butterfly Garden</b> 🌸 (Page {page+1}/{total_pages})\n\n"
    
    if filter_rarity:
        harem_message += f"<blockquote>🎯 <b>Rarity:</b> {filter_rarity}</blockquote>\n"
    
    harem_message += "<blockquote>"
    current_characters = unique_characters[page * 15:(page + 1) * 15]
    current_grouped = {k: list(v) for k, v in groupby(current_characters, key=lambda x: x['anime'])}
    
    for anime, chars in current_grouped.items():
        harem_message += f'\n🔮 <b>{anime}</b> ({len(chars)})\n'
        for char in chars:
            count = character_counts[char['id']]
            harem_message += f'  ◈⌠{char.get("rarity", "⭐")}⌡ <code>{char["id"]}</code> {char["name"]} <b>(x{count})</b>\n'
    harem_message += "</blockquote>"
    
    # Build keyboard
    keyboard = [
        [
            InlineKeyboardButton(f"🦋 Garden ({len(characters)})", switch_inline_query_current_chat=f"collection.{user_id}"),
        ]
    ]
    
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"harem:{page-1}:{user_id}:{filter_rarity or 'None'}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"harem:{page+1}:{user_id}:{filter_rarity or 'None'}"))
        keyboard.append(nav_buttons)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send or edit message
    if is_initial:
        await message.reply(harem_message, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        await callback_query.message.edit_text(harem_message, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
