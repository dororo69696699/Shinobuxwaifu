# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Claim Command - Daily free character claim
"""

from datetime import datetime, timedelta
from html import escape

from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_user, get_collection, update_user
from config import FORCE_JOIN_LINK

router = Router(name="claim")


@router.message(Command("hclaim", "claim"))
async def claim_command(message: Message) -> None:
    """Handle /claim or /hclaim command."""
    user_id = message.from_user.id
    today = datetime.utcnow().date()
    
    users_collection = get_collection("users")
    characters_collection = get_collection("characters")
    
    # Check if in force join channel
    # For now, skip force join check and just give character
    
    # Get user
    user = await users_collection.find_one({"id": user_id})
    if not user:
        user = {
            'id': user_id,
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'characters': [],
            'balance': 0
        }
        await users_collection.insert_one(user)
    
    # Check if already claimed today
    last_claimed = user.get('last_daily_reward')
    if last_claimed:
        if isinstance(last_claimed, str):
            last_claimed = datetime.fromisoformat(last_claimed)
        if last_claimed.date() == today:
            remaining = timedelta(days=1) - (datetime.utcnow() - last_claimed)
            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)
            await message.reply(
                f"🌸 You already claimed today! Come back in {hours}h {minutes}m.",
                parse_mode=ParseMode.HTML
            )
            return
    
    # Get a random character the user doesn't have
    claimed_ids = [char['id'] for char in user.get('characters', [])]
    
    pipeline = [
        {'$match': {'id': {'$nin': claimed_ids}}},
        {'$sample': {'size': 1}}
    ]
    cursor = characters_collection.aggregate(pipeline)
    characters = await cursor.to_list(length=None)
    
    if not characters:
        await message.reply(
            "🌸 The garden seems empty today. Please try again tomorrow!",
            parse_mode=ParseMode.HTML
        )
        return
    
    character = characters[0]
    
    # Add character to user
    await users_collection.update_one(
        {"id": user_id},
        {
            '$push': {'characters': character},
            '$set': {'last_daily_reward': datetime.utcnow()},
            '$inc': {'balance': 5}
        }
    )
    
    # Get updated balance
    updated_user = await users_collection.find_one({"id": user_id})
    balance = updated_user.get('balance', 0)
    
    await message.reply_photo(
        photo=character.get('img_url', ''),
        caption=(
            f"🌸 <b>Wisteria Blessing</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 <b>Hashira:</b> <a href='tg://user?id={user_id}'>{escape(message.from_user.first_name)}</a>\n"
            f"🌸 <b>Petals Earned:</b> +5\n"
            f"💰 <b>Total Petals:</b> {balance}\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"✨ <b>New Butterfly!</b>\n"
            f"📛 <b>Name:</b> {character.get('name', 'Unknown')}\n"
            f"🌈 <b>Rarity:</b> {character.get('rarity', 'Common')}\n"
            f"⛩️ <b>Anime:</b> {character.get('anime', 'Unknown')}"
        ),
        parse_mode=ParseMode.HTML
    )
