# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Redeem System - Generate and redeem codes
"""

import random
import string
from datetime import datetime
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from filters.admin import AdminOrVIPFilter
from database.models import get_collection, add_balance, get_user

router = Router(name="redeem")


@router.message(Command("gen"), AdminOrVIPFilter())
async def generate_code(message: Message) -> None:
    """Generate a redeem code (VIP/Admin only)."""
    redeem_collection = get_collection("redeem_codes")
    args = message.text.split()
    user_id = message.from_user.id
    
    if len(args) < 4:
        await message.reply(
            "Usage:\n"
            "`/gen coins <amount> <limit>` - Petal code\n"
            "`/gen <char_id> <copies> <limit>` - Character code\n\n"
            "Example: `/gen coins 5000 10`",
            parse_mode=ParseMode.HTML
        )
        return
    
    try:
        limit = int(args[-1])
        if limit <= 0 or limit > 1000:
            await message.reply("❌ Limit must be between 1 and 1000.")
            return
    except ValueError:
        await message.reply("❌ Invalid limit.")
        return
    
    if args[1].lower() == "coins":
        if len(args) != 4:
            await message.reply("Usage: `/gen coins <amount> <limit>`")
            return
        try:
            amount = int(args[2])
            if amount <= 0:
                raise ValueError
        except ValueError:
            await message.reply("❌ Invalid amount.")
            return
        
        reward_type = "coins"
        reward_data = amount
        reward_desc = f"{amount:,} petals"
    else:
        char_id = args[1]
        try:
            copies = int(args[2])
            if copies <= 0 or copies > 100:
                raise ValueError
        except ValueError:
            await message.reply("❌ Copies must be between 1 and 100.")
            return
        
        chars_collection = get_collection("characters")
        char = await chars_collection.find_one({'id': char_id})
        if not char:
            await message.reply(f"❌ Character '{char_id}' not found.")
            return
        
        reward_type = "character"
        reward_data = {"character_id": char_id, "copies": copies}
        reward_desc = f"{copies}x {char.get('name', 'Unknown')}"
    
    # Generate unique code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    while await redeem_collection.find_one({"code": code}):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    await redeem_collection.insert_one({
        "code": code,
        "reward_type": reward_type,
        "reward_data": reward_data,
        "reward_description": reward_desc,
        "creator_id": user_id,
        "created_at": datetime.utcnow(),
        "limit": limit,
        "redeemed_count": 0,
        "redeemed_by": [],
        "is_active": True
    })
    
    await message.reply(
        f"✅ <b>Code Generated!</b>\n\n"
        f"🎟 Code: <code>{code}</code>\n"
        f"📦 Reward: {reward_desc}\n"
        f"👥 Limit: {limit} users\n\n"
        f"Users redeem with <code>/redeem {code}</code>",
        parse_mode=ParseMode.HTML
    )


@router.message(Command("redeem"))
async def redeem_code(message: Message) -> None:
    """Redeem a code."""
    redeem_collection = get_collection("redeem_codes")
    args = message.text.split()
    user_id = message.from_user.id
    
    if len(args) < 2:
        await message.reply("Usage: `/redeem <code>`", parse_mode=ParseMode.HTML)
        return
    
    code = args[1]
    
    # April fool joke
    if code == "1APRGIFT":
        await message.reply("🤣 Happy April Fool! 🎉")
        return
    
    redeem_data = await redeem_collection.find_one({"code": code})
    if not redeem_data:
        await message.reply("❌ Invalid code.", parse_mode=ParseMode.HTML)
        return
    
    if not redeem_data.get("is_active", True):
        await message.reply("❌ Code is deactivated.", parse_mode=ParseMode.HTML)
        return
    
    if user_id in redeem_data.get("redeemed_by", []):
        await message.reply("❌ You already redeemed this code.", parse_mode=ParseMode.HTML)
        return
    
    if redeem_data.get("redeemed_count", 0) >= redeem_data.get("limit", 1):
        await message.reply("❌ Code limit reached.", parse_mode=ParseMode.HTML)
        return
    
    reward_type = redeem_data.get("reward_type")
    reward_data = redeem_data.get("reward_data")
    
    if reward_type == "coins":
        amount = int(reward_data)
        await add_balance(user_id, amount)
        
        await redeem_collection.update_one(
            {"code": code},
            {"$push": {"redeemed_by": user_id}, "$inc": {"redeemed_count": 1}}
        )
        
        await message.reply(
            f"✅ <b>Redeemed!</b>\n\n"
            f"🌸 +{amount:,} petals!",
            parse_mode=ParseMode.HTML
        )
    
    elif reward_type == "character":
        char_id = reward_data.get("character_id")
        copies = reward_data.get("copies", 1)
        
        chars_collection = get_collection("characters")
        char = await chars_collection.find_one({'id': char_id})
        if not char:
            await message.reply("❌ Character not found.")
            return
        
        users_collection = get_collection("users")
        # Efficient batch array push using $each
        await users_collection.update_one(
            {"id": user_id},
            {"$push": {"characters": {"$each": [char] * copies}}},
            upsert=True
        )
        
        await redeem_collection.update_one(
            {"code": code},
            {"$push": {"redeemed_by": user_id}, "$inc": {"redeemed_count": 1}}
        )
        
        await message.reply(
            f"✅ <b>Redeemed!</b>\n\n"
            f"🎭 {copies}x {char.get('name', 'Unknown')}\n"
            f"📺 {char.get('anime', 'Unknown')}\n"
            f"🌈 {char.get('rarity', 'Unknown')}",
            parse_mode=ParseMode.HTML
        )
    else:
        await message.reply("❌ Unknown reward type.", parse_mode=ParseMode.HTML)
