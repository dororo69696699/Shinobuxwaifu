# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Sudo User Management - Admin power management
"""

from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from filters.admin import AdminOrVIPFilter, OwnerFilter
from database.models import get_collection
from config import OWNER_ID

router = Router(name="sudo")

sudo_collection = get_collection("sudo_users")

ALL_POWERS = ["add", "del", "up", "app", "inv", "VIP"]


@router.message(Command("sudolist"), OwnerFilter())
async def sudo_list(message: Message) -> None:
    """List all sudo users (Owner only)."""
    cursor = sudo_collection.find({})
    users = await cursor.to_list(length=None)
    
    if not users:
        await message.reply("No sudo users found.", parse_mode=ParseMode.HTML)
        return
    
    text = "🛠 <b>Sudo Users:</b>\n\n"
    for user in users:
        user_id = user.get('_id')
        powers = user.get('powers', {})
        power_list = [p for p, v in powers.items() if v]
        text += f"• <a href='tg://user?id={user_id}'>{user_id}</a>: {', '.join(power_list)}\n"
    
    await message.reply(text, parse_mode=ParseMode.HTML)


@router.message(Command("addsudo"), AdminOrVIPFilter())
async def add_sudo(message: Message) -> None:
    """Add sudo user (VIP only)."""
    if not message.reply_to_message:
        await message.reply("Reply to a user to add them as sudo.", parse_mode=ParseMode.HTML)
        return
    
    user_id = message.reply_to_message.from_user.id
    
    existing = await sudo_collection.find_one({"_id": user_id})
    if existing:
        await message.reply(f"User <code>{user_id}</code> is already a sudo.", parse_mode=ParseMode.HTML)
        return
    
    await sudo_collection.update_one(
        {"_id": user_id},
        {"$set": {"powers": {"add": True}}},
        upsert=True
    )
    
    await message.reply(f"✅ User <code>{user_id}</code> added as sudo with 'add' power.", parse_mode=ParseMode.HTML)


@router.message(Command("removesudo"), AdminOrVIPFilter())
async def remove_sudo(message: Message) -> None:
    """Remove sudo user (VIP only)."""
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.text.split()) > 1 and message.text.split()[1].isdigit():
        user_id = int(message.text.split()[1])
    else:
        await message.reply("Reply to a user or provide a user ID.", parse_mode=ParseMode.HTML)
        return
    
    result = await sudo_collection.delete_one({"_id": user_id})
    if result.deleted_count > 0:
        await message.reply(f"✅ User <code>{user_id}</code> removed from sudo.", parse_mode=ParseMode.HTML)
    else:
        await message.reply(f"❌ User <code>{user_id}</code> is not a sudo.", parse_mode=ParseMode.HTML)


@router.message(Command("editsudo"), AdminOrVIPFilter())
async def edit_sudo(message: Message) -> None:
    """Edit sudo powers (VIP only)."""
    if not message.reply_to_message:
        await message.reply("Reply to a sudo user to edit their powers.", parse_mode=ParseMode.HTML)
        return
    
    user_id = message.reply_to_message.from_user.id
    user_data = await sudo_collection.find_one({"_id": user_id})
    
    if not user_data:
        await message.reply("User is not a sudo.", parse_mode=ParseMode.HTML)
        return
    
    powers = user_data.get("powers", {})
    buttons = []
    for power in ALL_POWERS:
        status = "✅" if powers.get(power, False) else "❌"
        buttons.append([
            InlineKeyboardButton(f"{power}", callback_data="noop"),
            InlineKeyboardButton(f"{status}", callback_data=f"toggle_power_{user_id}_{power}")
        ])
    buttons.append([InlineKeyboardButton("🔒 Close", callback_data="close_keyboard")])
    
    await message.reply(
        f"Edit powers for <code>{user_id}</code>:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(lambda c: c.data.startswith("toggle_power_"))
async def toggle_power(callback: CallbackQuery) -> None:
    """Toggle sudo power."""
    data = callback.data.split("_")
    user_id = int(data[2])
    power = data[3]
    
    user_data = await sudo_collection.find_one({"_id": user_id})
    if not user_data:
        await callback.answer("User not found!", show_alert=True)
        return
    
    current = user_data.get("powers", {}).get(power, False)
    new_status = not current
    
    await sudo_collection.update_one(
        {"_id": user_id},
        {"$set": {f"powers.{power}": new_status}}
    )
    
    await callback.answer(f"Power '{power}' set to {new_status}", show_alert=True)
    
    # Refresh keyboard
    powers = user_data.get("powers", {})
    powers[power] = new_status
    buttons = []
    for p in ALL_POWERS:
        status = "✅" if powers.get(p, False) else "❌"
        buttons.append([
            InlineKeyboardButton(f"{p}", callback_data="noop"),
            InlineKeyboardButton(f"{status}", callback_data=f"toggle_power_{user_id}_{p}")
        ])
    buttons.append([InlineKeyboardButton("🔒 Close", callback_data="close_keyboard")])
    
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


@router.callback_query(lambda c: c.data == "close_keyboard")
async def close_keyboard(callback: CallbackQuery) -> None:
    """Close sudo edit keyboard."""
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
