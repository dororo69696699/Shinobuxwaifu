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
    args = message.text.split()
    if len(args) != 2:
        await message.reply("Usage: <code>/gdelete ID</code>", parse_mode=ParseMode.HTML)
        return
    
    character_id = args[1]
    characters_collection = get_collection("characters")
    users_collection = get_collection("users")
    
    result = await characters_collection.delete_one({'id': character_id})
    if result.deleted_count == 0:
        await message.reply(f"Character with ID {character_id} not found.")
        return
    
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
    args = message.text.split()
    if len(args) != 4:
        await message.reply(
            "Usage: <code>/gupdate id field new_value</code>\n"
            "Fields: name, anime, rarity",
            parse_mode=ParseMode.HTML
        )
        return
    
    character_id, field, new_value = args[1], args[2], args[3]
    valid_fields = ['name', 'anime', 'rarity']
    
    if field not in valid_fields:
        await message.reply(f"Invalid field. Use: {', '.join(valid_fields)}")
        return
    
    if field == 'rarity':
        try:
            new_value = RARITY_MAP[int(new_value)]
        except (KeyError, ValueError):
            await message.reply("Invalid rarity number.")
            return
    
    characters_collection = get_collection("characters")
    users_collection = get_collection("users")
    
    result = await characters_collection.update_one(
        {'id': character_id},
        {'$set': {field: new_value}}
    )
    
    if result.modified_count == 0:
        await message.reply("Character not found or no changes made.")
        return
    
    await users_collection.update_many(
        {'characters.id': character_id},
        {'$set': {f'characters.$.{field}': new_value}}
    )
    
    await message.reply(f"✅ Character {character_id} updated successfully!")
