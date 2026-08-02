# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Upload Command - Add new character (Admin only)
"""

import os
import base64
import aiohttp
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from filters.admin import AdminOrVIPFilter
from database.models import get_collection
from assets.rarities import RARITY_MAP

router = Router(name="upload")


@router.message(Command("upload"), AdminOrVIPFilter())
async def upload_command(message: Message) -> None:
    """Handle /upload command."""
    args = message.text.split()
    if len(args) != 4:
        await message.reply(
            "Usage: `/upload name anime rarity_number`\n"
            "Reply to an image with this command.",
            parse_mode=ParseMode.HTML
        )
        return
    
    if not message.reply_to_message:
        await message.reply("Please reply to an image.", parse_mode=ParseMode.HTML)
        return
    
    name = args[1].replace('-', ' ').title()
    anime = args[2].replace('-', ' ').title()
    
    try:
        rarity = int(args[3])
        if rarity not in RARITY_MAP:
            raise ValueError
    except ValueError:
        await message.reply("Invalid rarity number. Check /rarity for valid numbers.")
        return
    
    # Get image from reply
    photo = message.reply_to_message.photo
    if not photo:
        await message.reply("Please reply to an image file.")
        return
    
    # Download image
    file = await message.bot.get_file(photo[-1].file_id)
    file_path = await file.download()
    
    try:
        # Upload to ImgBB
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.imgbb.com/1/upload",
                data={"key": "your_imgbb_key", "image": encoded}
            ) as resp:
                data = await resp.json()
                if data.get("success"):
                    img_url = data["data"]["url"]
                else:
                    await message.reply("Failed to upload image.")
                    return
        
        # Find next ID
        characters_collection = get_collection("characters")
        last = await characters_collection.find_one(sort=[("id", -1)])
        next_id = str(int(last.get("id", 0)) + 1).zfill(2) if last else "01"
        
        character = {
            "id": next_id,
            "name": name,
            "anime": anime,
            "rarity": RARITY_MAP[rarity],
            "rarity_number": rarity,
            "img_url": img_url
        }
        
        await characters_collection.insert_one(character)
        
        await message.reply(
            f"✅ <b>Character Uploaded!</b>\n\n"
            f"📛 Name: {name}\n"
            f"⛩️ Anime: {anime}\n"
            f"💎 Rarity: {RARITY_MAP[rarity]}\n"
            f"🆔 ID: {next_id}",
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        await message.reply(f"❌ Upload failed: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
