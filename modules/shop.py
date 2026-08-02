# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Shop System - Buy premium characters with wisteria petals
"""

import random
from datetime import datetime
from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_collection, get_user, add_balance, update_user
from config import OWNER_ID

router = Router(name="shop")

# Collections
shop_stock_collection = get_collection("shop_stock")
discounts_collection = get_collection("discounts")

# Rarity prices
RARITY_PRICE = {
    "⚪️ Common": 1000,
    "🟣 Rare": 5000,
    "🟢 Medium": 15000,
    "🟡 Legendary": 30000,
    "💮 Special Edition": 50000,
    "🔮 Limited Edition": 75000,
    "💸 Premium": 200000,
    "🌤 Summer": 80000,
    "🎐 Enchanted": 75000,
    "❄️ Frozen": 80000,
    "💝 Romantic": 85000,
    "🎃 Haunted": 75000,
    "🎄 Christmas": 70000,
    "🧧 Festive": 100000,
    "🍑 Naughty": 100000,
    "🎗️ AMV": 200000,
    "🌧 Cloudy": 80000,
    "🦠 Mythgard": 500000,
}

PREMIUM_RARITY = "💸 Premium Edition"
DEFAULT_DISCOUNT = 9


async def get_active_discount():
    """Get current active discount."""
    discount = await discounts_collection.find_one({})
    if discount and discount.get("expires_at", datetime.utcnow()) > datetime.utcnow():
        return discount.get("percent", DEFAULT_DISCOUNT)
    return DEFAULT_DISCOUNT


def is_video(url):
    """Check if URL is a video."""
    return any(url.lower().endswith(ext) for ext in [".mp4", ".mov", ".webm"])


# User shop state
user_shop_state = {}


@router.message(Command(["shop", "hshop", "hshopmenu"]))
async def shop_menu(message: Message) -> None:
    """Open shop menu."""
    user_id = message.from_user.id
    
    characters_collection = get_collection("characters")
    
    # Get all premium characters with stock
    all_premium = await characters_collection.find({"rarity": PREMIUM_RARITY}).to_list(None)
    
    if not all_premium:
        await message.reply(
            "🌸 No premium spirits available!\n\nPlease check back later.",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Get stock
    char_ids = [char['id'] for char in all_premium]
    stock_entries = await shop_stock_collection.find(
        {'character_id': {'$in': char_ids}, 'stock': {'$gt': 0}}
    ).to_list(None)
    
    stock_dict = {entry['character_id']: entry['stock'] for entry in stock_entries}
    price_dict = {entry['character_id']: entry.get('price', RARITY_PRICE.get(PREMIUM_RARITY, 120000)) for entry in stock_entries}
    
    characters = [char for char in all_premium if char['id'] in stock_dict]
    
    if not characters:
        await message.reply(
            "🌸 No premium spirits in stock!\n\nPlease check back later.",
            parse_mode=ParseMode.HTML
        )
        return
    
    random.shuffle(characters)
    
    user = await get_user(user_id)
    balance = user.get('balance', 0) if user else 0
    
    user_shop_state[user_id] = {
        "index": 0,
        "characters": characters,
        "stock_dict": stock_dict,
        "price_dict": price_dict,
        "balance": balance,
    }
    
    await display_shop_character(message, user_id, is_initial=True)


async def display_shop_character(message, user_id, is_initial=False, callback_query=None):
    """Display a single shop character."""
    state = user_shop_state.get(user_id)
    if not state:
        return
    
    index = state["index"]
    characters = state["characters"]
    stock_dict = state["stock_dict"]
    price_dict = state.get("price_dict", {})
    
    if index >= len(characters):
        index = 0
        state["index"] = 0
    
    char = characters[index]
    char_id = char.get('id')
    stock_count = stock_dict.get(char_id, 0)
    price = price_dict.get(char_id, RARITY_PRICE.get(PREMIUM_RARITY, 120000))
    
    discount = await get_active_discount()
    discounted_price = int(price * (100 - discount) / 100)
    
    user = await get_user(user_id)
    balance = user.get('balance', 0) if user else 0
    state["balance"] = balance
    
    can_afford = balance >= discounted_price and stock_count > 0
    
    caption = (
        f"🌸 <b>Wisteria Bazaar</b> 🌸\n\n"
        f"✨ <b>Name:</b> {char.get('name', 'Unknown')}\n"
        f"⛩️ <b>Anime:</b> {char.get('anime', 'Unknown')}\n"
        f"🌟 <b>Rarity:</b> {char.get('rarity', 'Premium')}\n"
        f"🌸 <b>Price:</b> <code>{discounted_price:,}</code> petals"
        f"{f' ({discount}% off)' if discount > 0 else ''}\n"
        f"📦 <b>Stock:</b> {stock_count}\n"
        f"💳 <b>Your Petals:</b> <code>{balance:,}</code>"
    )
    
    # Navigation buttons
    nav_buttons = []
    if index > 0:
        nav_buttons.append(InlineKeyboardButton("◀️ Prev", callback_data=f"shop_prev_{user_id}"))
    nav_buttons.append(InlineKeyboardButton(f"{index + 1}/{len(characters)}", callback_data="shop_noop"))
    if index < len(characters) - 1:
        nav_buttons.append(InlineKeyboardButton("Next ▶️", callback_data=f"shop_next_{user_id}"))
    
    keyboard = [nav_buttons] if nav_buttons else []
    
    # Buy button
    if can_afford:
        keyboard.append([InlineKeyboardButton(f"🌸 Buy ({discounted_price:,} petals)", callback_data=f"shop_buy_{user_id}_{index}")])
    elif stock_count == 0:
        keyboard.append([InlineKeyboardButton("🔒 Out of Stock", callback_data="shop_noop")])
    else:
        keyboard.append([InlineKeyboardButton(f"🔒 Need {discounted_price - balance:,} more", callback_data="shop_noop")])
    
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    img_url = char.get("img_url", "")
    
    if is_initial:
        await message.reply_photo(
            photo=img_url,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    else:
        await callback_query.message.edit_caption(
            caption=caption,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith("shop_next_"))
async def shop_next(callback: CallbackQuery) -> None:
    """Next shop item."""
    user_id = int(callback.data.split("_")[2])
    if callback.from_user.id != user_id:
        await callback.answer("Not your shop!", show_alert=True)
        return
    state = user_shop_state.get(user_id)
    if not state:
        await callback.answer("Session expired!", show_alert=True)
        return
    if state["index"] >= len(state["characters"]) - 1:
        await callback.answer("Last item!", show_alert=True)
        return
    state["index"] += 1
    await display_shop_character(callback.message, user_id, is_initial=False, callback_query=callback)


@router.callback_query(lambda c: c.data.startswith("shop_prev_"))
async def shop_prev(callback: CallbackQuery) -> None:
    """Previous shop item."""
    user_id = int(callback.data.split("_")[2])
    if callback.from_user.id != user_id:
        await callback.answer("Not your shop!", show_alert=True)
        return
    state = user_shop_state.get(user_id)
    if not state:
        await callback.answer("Session expired!", show_alert=True)
        return
    if state["index"] <= 0:
        await callback.answer("First item!", show_alert=True)
        return
    state["index"] -= 1
    await display_shop_character(callback.message, user_id, is_initial=False, callback_query=callback)


@router.callback_query(lambda c: c.data.startswith("shop_buy_"))
async def shop_buy(callback: CallbackQuery) -> None:
    """Buy shop item."""
    data = callback.data.split("_")
    user_id = int(data[2])
    index = int(data[3])
    
    if callback.from_user.id != user_id:
        await callback.answer("Not your shop!", show_alert=True)
        return
    
    state = user_shop_state.get(user_id)
    if not state or index != state["index"]:
        await callback.answer("Item changed!", show_alert=True)
        return
    
    char = state["characters"][index]
    char_id = char.get('id')
    
    stock_entry = await shop_stock_collection.find_one({'character_id': char_id})
    if not stock_entry or stock_entry.get('stock', 0) <= 0:
        await callback.answer("Out of stock!", show_alert=True)
        return
    
    user = await get_user(user_id)
    if not user:
        await callback.answer("User not found!", show_alert=True)
        return
    
    price = stock_entry.get('price', RARITY_PRICE.get(PREMIUM_RARITY, 120000))
    discount = await get_active_discount()
    discounted_price = int(price * (100 - discount) / 100)
    
    if user.get('balance', 0) < discounted_price:
        await callback.answer("Insufficient petals!", show_alert=True)
        return
    
    # Check if already owned
    for existing in user.get('characters', []):
        if existing.get('id') == char_id:
            await callback.answer("Already own this!", show_alert=True)
            return
    
    # Process purchase
    new_stock = stock_entry['stock'] - 1
    if new_stock == 0:
        await shop_stock_collection.delete_one({'character_id': char_id})
        state["stock_dict"][char_id] = 0
    else:
        await shop_stock_collection.update_one(
            {'character_id': char_id},
            {'$set': {'stock': new_stock}}
        )
        state["stock_dict"][char_id] = new_stock
    
    # Add to user
    users_collection = get_collection("users")
    await users_collection.update_one(
        {"id": user_id},
        {
            "$inc": {"balance": -discounted_price},
            "$push": {"characters": char}
        }
    )
    
    await callback.answer(f"🎉 {char.get('name')} added to your garden!", show_alert=True)
    
    # Remove from list if stock 0
    if new_stock == 0:
        state["characters"].pop(index)
        if state["index"] >= len(state["characters"]):
            state["index"] = len(state["characters"]) - 1
        
        if not state["characters"]:
            await callback.message.edit_caption(
                caption="🌸 All spirits have found new homes!\n\nPlease check back later.",
                reply_markup=None,
                parse_mode=ParseMode.HTML
            )
            return
    
    await display_shop_character(callback.message, user_id, is_initial=False, callback_query=callback)


@router.callback_query(lambda c: c.data == "shop_noop")
async def shop_noop(callback: CallbackQuery) -> None:
    """No operation callback."""
    await callback.answer()
