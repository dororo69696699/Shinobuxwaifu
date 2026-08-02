# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Jackpot Dice Game - Roll dice to earn coins
"""

from datetime import datetime, date
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_user, update_user, add_balance

router = Router(name="jackpot")


@router.message(Command("jackpot"))
async def jackpot_command(message: Message) -> None:
    """Handle /jackpot command."""
    user_id = message.from_user.id
    today = date.today()
    
    user = await get_user(user_id)
    if not user:
        user = {'id': user_id, 'balance': 0, 'plays_today': 0, 'last_played': None}
    
    last_played = user.get('last_played')
    plays_today = user.get('plays_today', 0)
    
    # Check play limit (2 per day)
    if last_played == str(today) and plays_today >= 2:
        await message.reply(
            "🎰 <b>Jackpot</b>\n\n"
            "<blockquote>❌ You can only play twice per day! Try again tomorrow.</blockquote>",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Send dice
    dice = await message.answer_dice("🎰")
    dice_score = dice.dice.value
    
    # Calculate reward
    if dice_score == 64:
        reward = 2000
    else:
        reward = 5 * dice_score
    
    # Update user
    if last_played == str(today):
        await update_user(user_id, {
            "last_played": str(today),
            "plays_today": plays_today + 1
        })
    else:
        await update_user(user_id, {
            "last_played": str(today),
            "plays_today": 1
        })
    
    await add_balance(user_id, reward)
    new_balance = await get_user_balance(user_id)
    
    await message.reply(
        f"🎰 <b>Jackpot Result</b>\n\n"
        f"👤 Player: {message.from_user.first_name}\n"
        f"<blockquote>🎲 Score: {dice_score}\n"
        f"🌸 Earned: +{reward} petals 🎉\n"
        f"💳 New Balance: {new_balance}</blockquote>",
        parse_mode=ParseMode.HTML
    )
