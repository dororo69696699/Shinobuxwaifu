# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Rank Command - Leaderboard
"""

import html
from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_collection

router = Router(name="rank")


@router.message(Command("rank"))
async def rank_command(message: Message) -> None:
    """Handle /rank command."""
    users_collection = get_collection("users")
    groups_collection = get_collection("top_global_groups")
    
    # Top users by character count
    cursor = users_collection.find({}, {"id": 1, "first_name": 1, "characters": 1})
    users = await cursor.to_list(length=None)
    users.sort(key=lambda x: len(x.get('characters', [])), reverse=True)
    top_users = users[:10]
    
    caption = "<b>TOP 10 USERS - MOST CHARACTERS</b>\n\n"
    for i, user in enumerate(top_users, 1):
        user_id = user.get('id', 0)
        first_name = html.escape(user.get('first_name', 'Unknown')[:15])
        count = len(user.get('characters', []))
        caption += f'{i}. <a href="tg://user?id={user_id}">{first_name}</a> ➾ <b>{count}</b>\n'
    
    buttons = [
        [
            InlineKeyboardButton("✅ Top", callback_data="top"),
            InlineKeyboardButton("Top Group", callback_data="top_group"),
        ],
        [
            InlineKeyboardButton("MTOP", callback_data="mtop"),
            InlineKeyboardButton("Tokens", callback_data="tokens"),
        ],
    ]
    
    await message.reply_photo(
        photo="https://files.catbox.moe/20xca5.jpg",
        caption=caption,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(lambda c: c.data == "top")
async def top_callback(callback) -> None:
    """Top users callback."""
    users_collection = get_collection("users")
    cursor = users_collection.find({}, {"id": 1, "first_name": 1, "characters": 1})
    users = await cursor.to_list(length=None)
    users.sort(key=lambda x: len(x.get('characters', [])), reverse=True)
    top_users = users[:10]
    
    caption = "<b>TOP 10 USERS - MOST CHARACTERS</b>\n\n"
    for i, user in enumerate(top_users, 1):
        user_id = user.get('id', 0)
        first_name = html.escape(user.get('first_name', 'Unknown')[:15])
        count = len(user.get('characters', []))
        caption += f'{i}. <a href="tg://user?id={user_id}">{first_name}</a> ➾ <b>{count}</b>\n'
    
    buttons = [
        [InlineKeyboardButton("✅ Top", callback_data="top"), InlineKeyboardButton("Top Group", callback_data="top_group")],
        [InlineKeyboardButton("MTOP", callback_data="mtop"), InlineKeyboardButton("Tokens", callback_data="tokens")]
    ]
    
    await callback.message.edit_caption(
        caption=caption,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "top_group")
async def top_group_callback(callback) -> None:
    """Top groups callback."""
    groups_collection = get_collection("top_global_groups")
    cursor = groups_collection.find({}).sort("count", -1).limit(10)
    groups = await cursor.to_list(length=10)
    
    caption = "<b>TOP 10 GROUPS - MOST GUESSES</b>\n\n"
    for i, group in enumerate(groups, 1):
        name = html.escape(group.get('group_name', 'Unknown')[:15])
        count = group.get('count', 0)
        caption += f'{i}. {name} ➾ <b>{count}</b>\n'
    
    buttons = [
        [InlineKeyboardButton("Top", callback_data="top"), InlineKeyboardButton("✅ Top Group", callback_data="top_group")],
        [InlineKeyboardButton("MTOP", callback_data="mtop"), InlineKeyboardButton("Tokens", callback_data="tokens")]
    ]
    
    await callback.message.edit_caption(
        caption=caption,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "mtop")
async def mtop_callback(callback) -> None:
    """MTOP (money top) callback."""
    users_collection = get_collection("users")
    cursor = users_collection.find({}).sort("balance", -1).limit(10)
    users = await cursor.to_list(length=10)
    
    caption = "<b>TOP 10 USERS - MOST PETALS</b>\n\n"
    for i, user in enumerate(users, 1):
        user_id = user.get('id', 0)
        first_name = html.escape(user.get('first_name', 'Unknown')[:15])
        balance = user.get('balance', 0)
        caption += f'{i}. <a href="tg://user?id={user_id}">{first_name}</a> ➾ <b>{balance:,}</b>\n'
    
    buttons = [
        [InlineKeyboardButton("Top", callback_data="top"), InlineKeyboardButton("Top Group", callback_data="top_group")],
        [InlineKeyboardButton("✅ MTOP", callback_data="mtop"), InlineKeyboardButton("Tokens", callback_data="tokens")]
    ]
    
    await callback.message.edit_caption(
        caption=caption,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "tokens")
async def tokens_callback(callback) -> None:
    """Tokens top callback."""
    users_collection = get_collection("users")
    cursor = users_collection.find({}).sort("tokens", -1).limit(10)
    users = await cursor.to_list(length=10)
    
    caption = "<b>TOP 10 USERS - MOST TOKENS</b>\n\n"
    for i, user in enumerate(users, 1):
        user_id = user.get('id', 0)
        first_name = html.escape(user.get('first_name', 'Unknown')[:15])
        tokens = user.get('tokens', 0)
        caption += f'{i}. <a href="tg://user?id={user_id}">{first_name}</a> ➾ <b>{tokens:,}</b>\n'
    
    buttons = [
        [InlineKeyboardButton("Top", callback_data="top"), InlineKeyboardButton("Top Group", callback_data="top_group")],
        [InlineKeyboardButton("MTOP", callback_data="mtop"), InlineKeyboardButton("✅ Tokens", callback_data="tokens")]
    ]
    
    await callback.message.edit_caption(
        caption=caption,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()
