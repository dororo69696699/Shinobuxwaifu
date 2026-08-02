# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Check Callbacks - Who Have It button
"""

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode

from database.models import get_collection

router = Router(name="check_callbacks")


@router.callback_query(lambda c: c.data.startswith("whohaveit_"))
async def who_have_it_callback(callback: CallbackQuery) -> None:
    """Handle Who Have It button."""
    character_id = callback.data.split("_")[1]
    
    users_collection = get_collection("users")
    users = await users_collection.find({'characters.id': character_id}).to_list(length=10)
    
    if not users:
        await callback.answer("No one owns this character yet!", show_alert=True)
        return
    
    owner_text = "**🏆 Top 10 Users Who Own This Character:**\n\n"
    for i, user in enumerate(users, 1):
        user_name = user.get('first_name', 'Unknown')
        count = sum(1 for char in user.get("characters", []) if char.get("id") == character_id)
        owner_text += f"{i}. [{user_name}](tg://user?id={user['id']}) — x{count}\n"
    
    await callback.answer()
    await callback.message.edit_caption(
        caption=f"{callback.message.caption}\n\n{owner_text}",
        reply_markup=None,
        parse_mode=ParseMode.MARKDOWN
    )
