# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Harem Callbacks - Navigation and filters
"""

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode

from modules.harem import display_harem

router = Router(name="harem_callbacks")


@router.callback_query(lambda c: c.data.startswith("harem:"))
async def harem_callback(callback: CallbackQuery) -> None:
    """Handle harem navigation callback."""
    _, page, user_id, filter_rarity = callback.data.split(':')
    page = int(page)
    user_id = int(user_id)
    filter_rarity = None if filter_rarity == 'None' else filter_rarity
    
    if callback.from_user.id != user_id:
        await callback.answer("This isn't your garden~", show_alert=True)
        return
    
    await callback.answer()
    await display_harem(callback.message, user_id, page, filter_rarity, is_initial=False, callback_query=callback)


@router.callback_query(lambda c: c.data.startswith("remove_filter:"))
async def remove_filter_callback(callback: CallbackQuery) -> None:
    """Handle remove filter callback."""
    _, user_id = callback.data.split(':')
    user_id = int(user_id)
    
    if callback.from_user.id != user_id:
        await callback.answer("This isn't your garden~", show_alert=True)
        return
    
    from database.models import get_collection
    users_collection = get_collection("users")
    await users_collection.update_one({"id": user_id}, {"$set": {"filter_rarity": None}}, upsert=True)
    
    await callback.answer("Filter removed!")
    await callback.message.delete()
