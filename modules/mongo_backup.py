# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
MongoDB Backup - Backup database to another MongoDB instance
"""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from motor.motor_asyncio import AsyncIOMotorClient
from filters.owner import OwnerFilter

router = Router(name="mongo_backup")


@router.message(Command("mongobackup"), OwnerFilter())
async def mongo_backup(message: Message) -> None:
    """Backup MongoDB to another instance (Owner only)."""
    args = message.text.split()
    
    if len(args) != 4:
        await message.reply(
            "Usage: `/mongobackup <source_uri> <dest_uri> <db_name>`\n\n"
            "Example: `/mongobackup mongodb://source:27017 mongodb://dest:27017 WAIFUBOT`",
            parse_mode=ParseMode.HTML
        )
        return
    
    source_uri, dest_uri, db_name = args[1], args[2], args[3]
    
    await message.reply("🔄 Starting backup...")
    
    try:
        source_client = AsyncIOMotorClient(source_uri)
        dest_client = AsyncIOMotorClient(dest_uri)
        
        source_db = source_client[db_name]
        dest_db = dest_client[db_name]
        
        collections = await source_db.list_collection_names()
        total_size = 0
        
        for collection_name in collections:
            await message.reply(f"📦 Backing up <code>{collection_name}</code>...", parse_mode=ParseMode.HTML)
            
            source_collection = source_db[collection_name]
            dest_collection = dest_db[collection_name]
            
            # Clear destination
            await dest_collection.delete_many({})
            
            # Copy documents
            docs = await source_collection.find({}).to_list(length=None)
            if docs:
                await dest_collection.insert_many(docs)
                size_bytes = sum(len(str(doc).encode()) for doc in docs)
                total_size += size_bytes
                size_mb = size_bytes / (1024 * 1024)
                await message.reply(
                    f"✅ <code>{collection_name}</code> - {size_mb:.2f} MB",
                    parse_mode=ParseMode.HTML
                )
            else:
                await message.reply(f"⚠️ <code>{collection_name}</code> is empty", parse_mode=ParseMode.HTML)
        
        total_mb = total_size / (1024 * 1024)
        await message.reply(
            f"✅ <b>Backup Complete!</b>\n\n"
            f"📊 Database: <code>{db_name}</code>\n"
            f"📦 Collections: {len(collections)}\n"
            f"💾 Total Size: {total_mb:.2f} MB",
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        await message.reply(f"❌ Backup failed: <code>{str(e)}</code>", parse_mode=ParseMode.HTML)
