import random
import time
from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

from config import START_MEDIA, SUPPORT_CHAT, UPDATE_CHAT, OWNER_USERNAME
from database.models import register_user

router = Router(name="start")


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    user = message.from_user
    await register_user(user.id, user.username, user.first_name, user.last_name)
    
    ping = round(time.time() - message.date.timestamp(), 2)
    caption = (
        f"🌸 <b>Welcome {user.first_name}!</b> 🌸\n\n"
        f"<i>I'm your waifu companion. Let's collect some anime characters!</i>\n\n"
        f"<blockquote>⚡ <b>Ping:</b> <code>{ping}s</code></blockquote>"
    )
    
    buttons = [
        [InlineKeyboardButton("🦋 Add to Group", url=f"https://t.me/{message.bot.username}?startgroup=true")],
        [
            InlineKeyboardButton("💜 Support", url=SUPPORT_CHAT),
            InlineKeyboardButton("📢 Updates", url=UPDATE_CHAT),
        ],
        [
            InlineKeyboardButton("🧪 Help", callback_data="open_help"),
            InlineKeyboardButton("👤 Owner", url=f"https://t.me/{OWNER_USERNAME}"),
        ]
    ]
    
    media = random.choice(START_MEDIA) if START_MEDIA else None
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    if not media:
        await message.reply(caption, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    elif media.lower().endswith(('.png', '.jpg', '.jpeg')):
        await message.reply_photo(photo=media, caption=caption, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    elif media.lower().endswith('.gif'):
        await message.reply_animation(animation=media, caption=caption, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await message.reply_video(video=media, caption=caption, reply_markup=keyboard, parse_mode=ParseMode.HTML)
