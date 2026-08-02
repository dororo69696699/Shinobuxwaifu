# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Update Commands - Update/Delete characters (Admin only)
"""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from filters.admin import AdminOrVIPFilter
from database.models import get_collection
from assets.rarities import RARITY_MAP

router = Router(name="update")


@router.message(Command("gdelete"), AdminOrVIPFilter())
async def delete_command(message: Message) -> None:
    """Handle /gdelete command."""
    args = message.text.split()
    if len(args) != 2:
        await message.reply("Usage: `/gdelete ID`", parse_mode=ParseMode.HTML)
        return
    
    character_id = args[1]
    characters_collection = get_collection("characters")
    users_collection = get_collection("users")
    
    # Delete character
    result = await characters_collection.delete_one({'id': character_id})
    if result.deleted_count == 0:
        await message.reply(f"Character with ID {character_id} not found.")
        return
    
    # Remove from all users
    update_result = await users_collection.update_many(
        {'characters.id': character_id},
        {'$pull': {'characters': {'id': character_id}}}
    )
    
    await message.reply(
        f"✅ Character {character_id} deleted.\n"
        f"Removed from {update_result.modified_count} users."
    )


@router.message(Command("gupdate"), AdminOrVIPFilter())
async def update_command(message: Message) -> None:
    """Handle /gupdate command."""
    args = message.text.split()
    if len(args) != 4:
        await message.reply(
            "Usage: `/gupdate id field new_value`\n"
            "Fields: name, anime, rarity",
            parse_mode=ParseMode.HTML
        )
        return
    
    character_id = args[1]
    field = args[2]
    new_value = args[3]
    
    valid_fields = ['name', 'anime', 'rarity']
    if field not in valid_fields:
        await message.reply(f"Invalid field. Use: {', '.join(valid_fields)}")
        return
    
    # Process rarity
    if field == 'rarity':
        try:
            new_value = RARITY_MAP[int(new_value)]
        except (KeyError, ValueError):
            await message.reply("Invalid rarity number.")
            return
    
    characters_collection = get_collection("characters")
    users_collection = get_collection("users")
    
    # Update character
    result = await characters_collection.update_one(
        {'id': character_id},
        {'$set': {field: new_value}}
    )
    
    if result.modified_count == 0:
        await message.reply("Character not found or no changes made.")
        return
    
    # Update all users
    await users_collection.update_many(
        {'characters.id': character_id},
        {'$set': {f'characters.$.{field}': new_value}}
    )
    
    await message.reply(f"✅ Character {character_id} updated successfully!")
