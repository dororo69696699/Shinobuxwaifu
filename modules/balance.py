import html
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.models import get_user_balance
from utils.cooldown import check_cooldown

router = Router(name="balance")


@router.message(Command("balance"))
async def balance_command(message: Message) -> None:
    user_id = message.from_user.id
    
    if not check_cooldown(user_id, "balance", 2):
        return
    
    balance = await get_user_balance(user_id)
    user_name = html.escape(message.from_user.first_name)
    
    await message.reply(
        f"🦋 <b>{user_name}'s Balance</b> 🌸\n\n"
        f"<blockquote>\n"
        f"🌸 <b>Wisteria Petals:</b> {balance}\n"
        f"</blockquote>",
        parse_mode="HTML",
    )
