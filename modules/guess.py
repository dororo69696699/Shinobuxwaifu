# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Guess Command - Guess the mystery character
"""

import time
from datetime import datetime
from html import escape

from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_user, update_user, get_collection
from utils.cooldown import check_cooldown

router = Router(name="guess")

# Global state (use database in production)
last_characters = {}
first_correct_guesses = {}
user_guess_progress = {}


@router.message(Command("guess", "protecc", "collect", "grab", "hunt"))
async def guess_command(message: Message) -> None:
    """Handle /guess command."""
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Check cooldown
    if not check_cooldown(user_id, "guess", 5):
        await message.reply("🌸 Please wait a moment before your next attempt!", parse_mode=ParseMode.HTML)
        return
    
    if chat_id not in last_characters:
        await message.reply("🌸 The garden is quiet. No spirits have manifested yet.", parse_mode=ParseMode.HTML)
        return
    
    if chat_id in first_correct_guesses:
        await message.reply("🌸 This butterfly has already been guided home!", parse_mode=ParseMode.HTML)
        return
    
    guess = ' '.join(message.text.split()[1:]).lower() if len(message.text.split()) > 1 else ''
    
    if not guess:
        await message.reply("Please provide a character name: `/guess <name>`", parse_mode=ParseMode.HTML)
        return
    
    character = last_characters[chat_id]
    name_parts = character.get('name', '').lower().split()
    guess_parts = guess.split()
    
    # Check if guess matches
    if sorted(name_parts) == sorted(guess_parts) or any(part == guess for part in name_parts):
        first_correct_guesses[chat_id] = user_id
        
        time_taken = int(time.time() - character.get('timestamp', time.time()))
        
        # Add character to user
        users_collection = get_collection("users")
        user = await users_collection.find_one({"id": user_id})
        
        if user:
            await users_collection.update_one({"id": user_id}, {"$push": {"characters": character}})
            await users_collection.update_one({"id": user_id}, {"$inc": {"balance": 40}})
        else:
            await users_collection.insert_one({
                'id': user_id,
                'username': message.from_user.username,
                'first_name': message.from_user.first_name,
                'characters': [character],
                'balance': 40
            })
        
        # Get updated balance
        updated_user = await users_collection.find_one({"id": user_id})
        new_balance = updated_user.get('balance', 0) if updated_user else 40
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("🦋 View Your Garden", switch_inline_query_current_chat=f"collection.{user_id}")]
        ])
        
        await message.reply(
            f"🌸 <b>Congratulations!</b>\n\n"
            f"<a href='tg://user?id={user_id}'>{escape(message.from_user.first_name)}</a>, you caught the spirit!\n\n"
            f"<blockquote>\n"
            f"📛 Name: {character.get('name', 'Unknown')}\n"
            f"⛩️ Anime: {character.get('anime', 'Unknown')}\n"
            f"💎 Rarity: {character.get('rarity', 'Common')}\n"
            f"⏱️ Time: {time_taken}s\n"
            f"💰 Reward: +40\n"
            f"💳 Balance: {new_balance}\n"
            f"</blockquote>",
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
    else:
        await message.reply(
            "🌸 Not quite! Take a closer look at the spirit's essence.",
            parse_mode=ParseMode.HTML
        )
