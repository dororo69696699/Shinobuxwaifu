from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models import get_collection

router = Router(name="total")


@router.message(Command("total"))
async def total_command(message: Message) -> None:
    characters_collection = get_collection("characters")
    total = await characters_collection.count_documents({})
    
    await message.reply(
        f"📊 <b>Total Characters in Bot:</b> <code>{total:,}</code>",
        parse_mode=ParseMode.HTML
    )
