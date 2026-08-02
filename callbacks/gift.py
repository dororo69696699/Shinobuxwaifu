# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Gift Callbacks - Confirm/Cancel gift
"""

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode

from database.models import get_user, update_user, get_collection
from modules.gift import pending_gifts

router = Router(name="gift_callbacks")


@router.callback_query(lambda c: c.data in ["confirm_gift", "cancel_gift"])
async def gift_callback(callback: CallbackQuery) -> None:
    """Handle gift confirm/cancel."""
    sender_id = callback.from_user.id
    
    # Find pending gift
    found_key = None
    gift = None
    for key, g in pending_gifts.items():
        if key[0] == sender_id:
            found_key = key
            gift = g
            break
    
    if not gift:
        await callback.answer("This is not for you!", show_alert=True)
        return
    
    receiver_id = found_key[1]
    
    if callback.data == "confirm_gift":
        if gift.get('processed', False):
            await callback.answer("This gift has already been processed.", show_alert=True)
            return
        
        gift['processed'] = True
        
        # Transfer character
        users_collection = get_collection("users")
        
        # Remove from sender
        sender = await users_collection.find_one({"id": sender_id})
        if sender:
            sender_chars = sender.get('characters', [])
            sender_chars = [c for c in sender_chars if c.get('id') != gift['character'].get('id')]
            await users_collection.update_one({"id": sender_id}, {"$set": {"characters": sender_chars}})
        
        # Add to receiver
        receiver = await users_collection.find_one({"id": receiver_id})
        if receiver:
            await users_collection.update_one({"id": receiver_id}, {"$push": {"characters": gift['character']}})
        else:
            await users_collection.insert_one({
                'id': receiver_id,
                'first_name': gift.get('receiver_name', 'User'),
                'characters': [gift['character']]
            })
        
        del pending_gifts[found_key]
        
        await callback.message.edit_caption(
            caption=f"🎉 <b>Gift Successful!</b>\n\nYou gifted your character to <a href='tg://user?id={receiver_id}'>{gift['receiver_name']}</a>!",
            reply_markup=None,
            parse_mode=ParseMode.HTML
        )
        await callback.answer("Gift sent successfully!")
    
    elif callback.data == "cancel_gift":
        del pending_gifts[found_key]
        await callback.message.edit_caption(
            caption="❌ Gift cancelled.",
            reply_markup=None,
            parse_mode=ParseMode.HTML
        )
        await callback.answer("Gift cancelled.")
