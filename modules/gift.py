# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Gift Command - Gift characters to other users
"""

import asyncio
from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_user, update_user, get_collection

router = Router(name="gift")

# Pending gifts storage
pending_gifts = {}


@router.message(Command("gift"))
async def gift_command(message: Message) -> None:
    """Handle /gift command."""
    sender_id = message.from_user.id
    
    # Check for existing pending gift
    for (s_id, _), gift in pending_gifts.items():
        if s_id == sender_id and not gift.get('processed', False):
            await message.reply(
                "You already have a gift processing. Please confirm or cancel it first.",
                parse_mode=ParseMode.HTML
            )
            return
    
    if not message.reply_to_message:
        await message.reply(
            "You need to reply to a user's message to gift a character!",
            parse_mode=ParseMode.HTML
        )
        return
    
    receiver_id = message.reply_to_message.from_user.id
    receiver_name = message.reply_to_message.from_user.first_name
    
    if sender_id == receiver_id:
        await message.reply("You can't gift a character to yourself!", parse_mode=ParseMode.HTML)
        return
    
    args = message.text.split()
    if len(args) != 2:
        await message.reply("You need to provide a character ID!", parse_mode=ParseMode.HTML)
        return
    
    character_id = args[1]
    sender = await get_user(sender_id)
    
    if not sender:
        await message.reply("You don't have any characters!", parse_mode=ParseMode.HTML)
        return
    
    # Find character
    character = next((c for c in sender.get('characters', []) if c.get('id') == character_id), None)
    if not character:
        await message.reply("You don't have this character in your collection!", parse_mode=ParseMode.HTML)
        return
    
    # Store pending gift
    pending_gifts[(sender_id, receiver_id)] = {
        'character': character,
        'receiver_name': receiver_name,
        'processed': False
    }
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("✅ Confirm Gift", callback_data="confirm_gift")],
        [InlineKeyboardButton("❌ Cancel Gift", callback_data="cancel_gift")]
    ])
    
    caption = f"🎁 <b>Gift Character</b>\n🌸 <b>{character.get('name', 'Unknown')}</b>"
    
    if character.get('img_url'):
        await message.reply_photo(photo=character['img_url'], caption=caption, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await message.reply(caption, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    
    # Auto-cancel after 1 hour
    asyncio.create_task(auto_cancel_gift(sender_id, receiver_id))


async def auto_cancel_gift(sender_id, receiver_id):
    """Auto-cancel gift after 1 hour."""
    await asyncio.sleep(3600)
    key = (sender_id, receiver_id)
    if key in pending_gifts and not pending_gifts[key].get('processed', False):
        del pending_gifts[key]
