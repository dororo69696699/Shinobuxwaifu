import html
from datetime import datetime
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import DAILY_REWARD
from database.models import get_user, update_user, add_balance
from utils.cooldown import check_cooldown

router = Router(name="daily")


@router.message(Command("daily"))
async def daily_command(message: Message) -> None:
    user_id = message.from_user.id
    
    if not check_cooldown(user_id, "daily", 5):
        await message.reply("⏰ Please wait before using this command again.")
        return
    
    user = await get_user(user_id)
    today = datetime.now().date()
    
    if user and user.get("last_daily"):
        last_daily = user["last_daily"]
        if isinstance(last_daily, str):
            last_daily = datetime.fromisoformat(last_daily).date()
        else:
            last_daily = last_daily.date()
        
        if last_daily == today:
            await message.reply("🌸 You already claimed your daily reward today! Come back tomorrow.")
            return
    
    await add_balance(user_id, DAILY_REWARD)
    await update_user(user_id, {"last_daily": datetime.now()})
    
    new_balance = await get_user_balance(user_id)
    user_name = html.escape(message.from_user.first_name)
    
    await message.reply(
        f"🦋 <b>Daily Reward</b> 🌸\n\n"
        f"<blockquote>\n"
        f"🌸 +{DAILY_REWARD} Wisteria Petals!\n"
        f"💳 New Balance: {new_balance}\n"
        f"</blockquote>",
        parse_mode="HTML",
    )
