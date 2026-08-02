import html
from datetime import datetime, timedelta
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import WEEKLY_REWARD
from database.models import get_user, update_user, add_balance
from utils.cooldown import check_cooldown

router = Router(name="weekly")


@router.message(Command("weekly"))
async def weekly_command(message: Message) -> None:
    user_id = message.from_user.id
    
    if not check_cooldown(user_id, "weekly", 5):
        await message.reply("⏰ Please wait before using this command again.")
        return
    
    user = await get_user(user_id)
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    if user and user.get("last_weekly"):
        last_weekly = user["last_weekly"]
        if isinstance(last_weekly, str):
            last_weekly = datetime.fromisoformat(last_weekly)
        
        if last_weekly >= week_start:
            next_week = week_start + timedelta(days=7)
            days_left = (next_week - now).days
            await message.reply(f"🌸 Weekly reward already claimed! Next in {days_left} days.")
            return
    
    await add_balance(user_id, WEEKLY_REWARD)
    await update_user(user_id, {"last_weekly": datetime.now()})
    
    new_balance = await get_user_balance(user_id)
    user_name = html.escape(message.from_user.first_name)
    
    await message.reply(
        f"🦋 <b>Weekly Reward</b> 🎉\n\n"
        f"<blockquote>\n"
        f"🌸 +{WEEKLY_REWARD} Wisteria Petals!\n"
        f"💳 New Balance: {new_balance}\n"
        f"</blockquote>",
        parse_mode="HTML",
    )
