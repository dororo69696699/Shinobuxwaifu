# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Wheel of Fortune - Spin the wheel to win coins or characters
"""

import random
import asyncio
from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_user, update_user, get_collection, add_balance

router = Router(name="wheel")

# Concurrency lock
active_spins = set()

# Wheel sectors: (name, multiplier/type, weight)
SECTORS = [
    ("❌ Bust (0.0x)", 0.0, 35),
    ("📉 Half Loss (0.5x)", 0.5, 20),
    ("⚖️ Push (1.0x)", 1.0, 15),
    ("📈 Win (1.5x)", 1.5, 15),
    ("🔥 Double (2.0x)", 2.0, 10),
    ("🚀 Jackpot (5.0x)", 5.0, 4),
    ("🌟 Waifu Drop", "waifu", 1)
]


def roll_wheel():
    """Roll the wheel and return selected sector."""
    sectors_list = []
    weights = []
    for sector in SECTORS:
        sectors_list.append(sector)
        weights.append(sector[2])
    return random.choices(sectors_list, weights=weights, k=1)[0]


async def get_drop_character():
    """Get a random legendary/celestial character for waifu drop."""
    characters_collection = get_collection("characters")
    pipeline = [
        {
            '$match': {
                'rarity': {'$in': ['🟡 Legendary', '🎐 Celestial', '🔮 Limited Edition', '💮 Special Edition']},
                'img_url': {'$exists': True, '$ne': ''},
                'id': {'$exists': True},
                'name': {'$exists': True, '$ne': ''},
                'anime': {'$exists': True, '$ne': ''}
            }
        },
        {'$sample': {'size': 1}}
    ]
    cursor = characters_collection.aggregate(pipeline)
    characters = await cursor.to_list(length=None)
    return characters[0] if characters else None


@router.message(Command(["wheel", "spin"]))
async def spin_wheel(message: Message) -> None:
    """Handle /spin or /wheel command."""
    user_id = message.from_user.id
    
    if user_id in active_spins:
        await message.reply(
            "🎡 <b>Wheel</b>\n\n"
            "<blockquote>⏳ Your previous spin is still processing!</blockquote>",
            parse_mode=ParseMode.HTML
        )
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.reply(
            "🎡 <b>Wheel of Fortune</b>\n\n"
            "<blockquote>🎮 <b>How to Play:</b>\n"
            "Use <code>/spin &lt;amount&gt;</code>\n\n"
            "🎰 <b>Sectors:</b>\n"
            "• Bust: 0.0x | Half: 0.5x | Push: 1.0x\n"
            "• Win: 1.5x | Double: 2.0x | Jackpot: 5.0x\n"
            "• Waifu Drop: Random Legendary!\n\n"
            "⚠️ Min: 100 | Max: 50,000</blockquote>",
            parse_mode=ParseMode.HTML
        )
        return
    
    try:
        amount = int(args[1])
        if amount < 100 or amount > 50000:
            await message.reply(
                "❌ Bet must be between 100 and 50,000!",
                parse_mode=ParseMode.HTML
            )
            return
    except ValueError:
        await message.reply("❌ Please enter a valid number!", parse_mode=ParseMode.HTML)
        return
    
    # Check balance
    balance = await get_user_balance(user_id)
    if balance < amount:
        await message.reply(
            f"❌ Insufficient balance! You have {balance} petals.",
            parse_mode=ParseMode.HTML
        )
        return
    
    active_spins.add(user_id)
    
    try:
        # Deduct bet
        await add_balance(user_id, -amount)
        
        status_msg = await message.reply(
            f"🎡 <b>Lucky Wheel Spin</b>\n\n"
            f"👤 Player: {message.from_user.first_name}\n"
            f"<blockquote>💰 Bet: {amount} petals\n\n"
            f"🌀 <b>[ 🔴 🔵 🟡 🟢 ]</b>\n\n"
            f"<i>Spinning...</i></blockquote>",
            parse_mode=ParseMode.HTML
        )
        
        # Animation frames
        frames = [
            "🌀 <b>[ 🔵 🟡 🟢 🔴 ]</b>",
            "🌀 <b>[ 🟡 🟢 🔴 🔵 ]</b>",
            "🌀 <b>[ 🟢 🔴 🔵 🟡 ]</b>"
        ]
        
        for frame in frames:
            await asyncio.sleep(0.5)
            await status_msg.edit_text(
                f"🎡 <b>Lucky Wheel Spin</b>\n\n"
                f"👤 Player: {message.from_user.first_name}\n"
                f"<blockquote>💰 Bet: {amount} petals\n\n"
                f"{frame}\n\n"
                f"<i>Spinning...</i></blockquote>",
                parse_mode=ParseMode.HTML
            )
        
        await asyncio.sleep(0.5)
        
        # Roll wheel
        selected_sector = roll_wheel()
        sector_name, outcome, _ = selected_sector
        
        if outcome == "waifu":
            character = await get_drop_character()
            if character:
                users_collection = get_collection("users")
                await users_collection.update_one(
                    {"id": user_id},
                    {"$push": {"characters": character}},
                    upsert=True
                )
                
                caption = (
                    f"🎡 <b>Lucky Wheel Spin</b>\n\n"
                    f"👤 Player: {message.from_user.first_name}\n"
                    f"<blockquote>✨ <b>{sector_name}!</b> ✨\n\n"
                    f"🎉 You won a character drop!\n"
                    f"🌸 Name: {character['name']}\n"
                    f"⛩️ Anime: {character['anime']}\n"
                    f"🌈 Rarity: {character['rarity']}\n"
                    f"🆔 ID: {character['id']}</blockquote>"
                )
                
                if character.get('img_url'):
                    await message.reply_photo(photo=character['img_url'], caption=caption, parse_mode=ParseMode.HTML)
                else:
                    await message.reply(caption, parse_mode=ParseMode.HTML)
                
                await status_msg.delete()
                return
            else:
                outcome = 5.0
                sector_name = "🚀 Jackpot (5.0x) (Waifu fallback)"
        
        if isinstance(outcome, float) or isinstance(outcome, int):
            winnings = int(amount * outcome)
            await add_balance(user_id, winnings)
            
            new_balance = await get_user_balance(user_id)
            
            if winnings > amount:
                status_text = f"🎉 Won! Net: +{winnings - amount} (Payout: {winnings})"
            elif winnings == amount:
                status_text = f"⚖️ Push! Bet refunded."
            elif winnings > 0:
                status_text = f"📉 Half Loss! Refunded: {winnings}"
            else:
                status_text = f"😭 Bust! Lost: -{amount}"
            
            await status_msg.edit_text(
                f"🎡 <b>Lucky Wheel Spin</b>\n\n"
                f"👤 Player: {message.from_user.first_name}\n"
                f"<blockquote>✨ <b>[ {sector_name} ]</b> ✨\n\n"
                f"{status_text}\n"
                f"💳 New Balance: {new_balance}</blockquote>",
                parse_mode=ParseMode.HTML
            )
            
    except Exception as e:
        print(f"Error in wheel spin: {e}")
        await add_balance(user_id, amount)
        await message.reply("⚠️ Error occurred. Refunded.", parse_mode=ParseMode.HTML)
    finally:
        active_spins.remove(user_id)
