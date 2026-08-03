
   import html
import asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_collection
from assets.rarities import RARITY_MAP

router = Router(name="stats")

STATS_IMG = ["https://files.catbox.moe/gknnju.jpg"]


async def get_user_stats(user_id: int):
    users_collection = get_collection("users")
    characters_collection = get_collection("characters")
    
    user_data = await users_collection.find_one(
        {'id': user_id},
        {'balance': 1, 'first_name': 1, 'characters': 1, 'tokens': 1}
    )
    if not user_data:
        return None, "User data not found."
    
    balance = user_data.get('balance', 0)
    tokens = user_data.get('tokens', 0)
    first_name = html.escape(user_data.get('first_name', 'Unknown'))
    characters = user_data.get('characters', [])
    
    total_characters = await characters_collection.count_documents({})
    character_count = len(characters)
    progress_percentage = (character_count / total_characters * 100) if total_characters > 0 else 0
    
    filled_slots = int(progress_percentage / 10)
    progress_bar = '█' * filled_slots + '□' * (10 - filled_slots)
    
    all_users = await users_collection.find({}, {"id": 1, "characters": 1}).to_list(length=None)
    all_users.sort(key=lambda x: len(x.get('characters', [])), reverse=True)
    total_users = len(all_users)
    rank = next((i + 1 for i, u in enumerate(all_users) if u.get('id') == user_id), total_users)
    
    rarity_counts = {rarity: 0 for rarity in RARITY_MAP.values()}
    for char in characters:
        char_rarity = char.get('rarity')
        if char_rarity in rarity_counts:
            rarity_counts[char_rarity] += 1
    
    return {
        'user_id': user_id,
        'first_name': first_name,
        'balance': balance,
        'tokens': tokens,
        'character_count': character_count,
        'total_characters': total_characters,
        'progress_percentage': progress_percentage,
        'progress_bar': progress_bar,
        'rank': rank,
        'total_users': total_users,
        'rarity_counts': rarity_counts
    }, None


@router.message(Command("stats"))
async def stats_command(message: Message) -> None:
    user_id = message.from_user.id
    processing = await message.reply_photo(
        photo=STATS_IMG[0],
        caption="🌸 Processing your garden data...",
        parse_mode=ParseMode.HTML
    )
    await asyncio.sleep(0.5)
    
    stats, error = await get_user_stats(user_id)
    if error:
        await processing.edit_caption(caption=error, parse_mode=ParseMode.HTML)
        return
    
    rarity_lines = []
    for rarity_name in RARITY_MAP.values():
        emoji = rarity_name.split()[0] if rarity_name.split() else "🌸"
        display_name = rarity_name.replace(emoji, '').strip()
        rarity_lines.append(f"{emoji} <b>{display_name}</b> ↬ {stats['rarity_counts'].get(rarity_name, 0)}")
    
    caption = (
        f"🦋 <b>Shinobu Garden</b>\n━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>Name</b> ↬ {stats['first_name']}\n"
        f"🆔 <b>User ID</b> ↬ {stats['user_id']}\n\n"
        f"🌸 <b>Wisteria Petals</b> ↬ {stats['balance']:,}\n"
        f"🎫 <b>Tokens</b> ↬ {stats['tokens']}\n"
        f"🦋 <b>Collection</b> ↬ {stats['character_count']}/{stats['total_characters']}\n"
        f"🏆 <b>Global Rank</b> ↬ #{stats['rank']}\n\n"
        f"📈 <b>Progress</b> ↬ {stats['progress_bar']} {stats['progress_percentage']:.1f}%\n"
        f"━━━━━━━━━━━━━━━━━━\n\n" + "\n".join(rarity_lines) +
        f"\n━━━━━━━━━━━━━━━━━━\n\n🌸\n<i>\"Every butterfly eventually finds\nits place beneath the wisteria.\"</i>\n\n💜 <b>Shinobu Kocho</b>"
    )
    await processing.edit_caption(caption=caption, parse_mode=ParseMode.HTML) 
   
