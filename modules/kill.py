from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.admin import AdminOrVIPFilter
from database.models import delete_user, get_user, update_user

router = Router(name="kill")


@router.message(Command("kill"), AdminOrVIPFilter())
async def kill_command(message: Message) -> None:
    args = message.text.split()
    
    if not message.reply_to_message:
        await message.reply("Please reply to a user's message.")
        return
    
    target_id = message.reply_to_message.from_user.id
    
    if len(args) < 2:
        await message.reply(
            "Usage:\n"
            "• <code>f</code> - Delete full data\n"
            "• <code>b [amount]</code> - Deduct balance",
            parse_mode="HTML",
        )
        return
    
    option = args[1]
    
    if option == 'f':
        await delete_user(target_id)
        await message.reply("✅ User data deleted.")
    
    elif option == 'b':
        if len(args) < 3:
            await message.reply("Specify an amount: /kill b 100")
            return
        try:
            amount = int(args[2])
            user = await get_user(target_id)
            if user:
                new_balance = max(0, user.get("balance", 0) - amount)
                await update_user(target_id, {"balance": new_balance})
                await message.reply(f"✅ Deducted {amount}. New balance: {new_balance}")
            else:
                await message.reply("❌ User not found.")
        except ValueError:
            await message.reply("❌ Invalid amount.")
    
    else:
        await message.reply("❌ Invalid option. Use <code>f</code> or <code>b</code>.")
