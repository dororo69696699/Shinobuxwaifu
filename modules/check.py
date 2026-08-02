# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Check Command - View character details
"""

from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_collection

router = Router(name="check")


@router.message(Command("check"))
async def check_command(message: Message) -> None:
    """Handle /check command."""
    args = message.text.split()
    if len(args) < 2:
        await message.reply("Please provide a Character ID: `/check <character_id>`", parse_mode=ParseMode.HTML)
        return
    
    character_id = args[1]
    characters_collection = get_collection("characters")
    character = await characters_collection.find_one({'id': character_id})
    
    if not character:
        await message.reply("Character not found.")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Who Have It", callback_data=f"whohaveit_{character_id}")]
    ])
    
    text = (
        f"🌟 <b>Character Info</b>\n"
        f"🆔 ID: <code>{character_id}</code>\n"
        f"📛 Name: {character.get('name', 'Unknown')}\n"
        f"📺 Anime: {character.get('anime', 'Unknown')}\n"
        f"💎 Rarity: {character.get('rarity', 'Unknown')}\n"
    )
    
    if character.get('vid_url'):
        await message.reply_video(character['vid_url'], caption=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await message.reply_photo(character.get('img_url', ''), caption=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
