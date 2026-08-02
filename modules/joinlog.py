# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Join/Leave Logger - Log when bot joins or leaves groups
"""

from aiogram import Router
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.enums import ParseMode

from config import BOT_LOGGING

router = Router(name="joinlog")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER))
async def bot_joined_group(event: ChatMemberUpdated) -> None:
    """Log when bot joins a group."""
    chat = event.chat
    user = event.from_user
    
    log_text = (
        f"#newgroup\n\n"
        f"📛 <b>Chat:</b> {chat.title or 'Unknown'}\n"
        f"🆔 <b>ID:</b> <code>{chat.id}</code>\n"
        f"👤 <b>Added by:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
        f"📅 <b>Time:</b> {event.date.strftime('%Y-%m-%d %H:%M:%S')} UTC"
    )
    
    try:
        await event.bot.send_message(
            chat_id=BOT_LOGGING,
            text=log_text,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        print(f"Failed to send join log: {e}")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> IS_NOT_MEMBER))
async def bot_left_group(event: ChatMemberUpdated) -> None:
    """Log when bot leaves a group."""
    chat = event.chat
    user = event.from_user
    
    log_text = (
        f"#leftgroup\n\n"
        f"📛 <b>Chat:</b> {chat.title or 'Unknown'}\n"
        f"🆔 <b>ID:</b> <code>{chat.id}</code>\n"
        f"👤 <b>Removed by:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
        f"📅 <b>Time:</b> {event.date.strftime('%Y-%m-%d %H:%M:%S')} UTC"
    )
    
    try:
        await event.bot.send_message(
            chat_id=BOT_LOGGING,
            text=log_text,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        print(f"Failed to send leave log: {e}")
