import html
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.models import get_user_balance, add_balance, get_user_by_username
from utils.cooldown import check_cooldown

router = Router(name="pay")


@router.message(Command("pay"))
async def pay_command(message: Message) -> None:
    sender_id = message.from_user.id
    args = message.text.split()
    
    if not check_cooldown(sender_id, "pay", 3):
        await message.reply("⏰ Please wait before sending another payment.")
        return
    
    if len(args) < 2:
        await message.reply("Usage: /pay <amount> [@username] or reply to a user.")
        return
    
    try:
        amount = int(args[1])
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.reply("❌ Invalid amount.")
        return
    
    recipient_id = None
    
    if message.reply_to_message:
        recipient_id = message.reply_to_message.from_user.id
    elif len(args) > 2:
        username = args[2].lstrip('@')
        user = await get_user_by_username(username)
        if user:
            recipient_id = user["id"]
    
    if not recipient_id:
        await message.reply("❌ Recipient not found.")
        return
    
    if recipient_id == sender_id:
        await message.reply("❌ You can't pay yourself!")
        return
    
    sender_balance = await get_user_balance(sender_id)
    if sender_balance < amount:
        await message.reply("❌ Insufficient balance.")
        return
    
    await add_balance(sender_id, -amount)
    await add_balance(recipient_id, amount)
    
    new_balance = await get_user_balance(sender_id)
    sender_name = html.escape(message.from_user.first_name)
    
    await message.reply(
        f"✅ You paid {amount} Wisteria Petals!\n"
        f"💳 New Balance: {new_balance}",
        parse_mode="HTML",
    )
    
    try:
        await message.bot.send_message(
            recipient_id,
            f"🌸 You received {amount} Wisteria Petals from {sender_name}!",
            parse_mode="HTML",
        )
    except:
        pass
