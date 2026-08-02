
import time
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.admin import AdminOrVIPFilter

router = Router(name="ping")


@router.message(Command("ping"), AdminOrVIPFilter())
async def ping_command(message: Message) -> None:
    start = time.perf_counter()
    sent = await message.reply("🏓 Pong!")
    elapsed = round((time.perf_counter() - start) * 1000, 2)
    await sent.edit_text(f"🏓 Pong! <code>{elapsed}ms</code>", parse_mode="HTML")


@router.message(Command("ping"))
async def ping_denied(message: Message) -> None:
    await message.reply("🚫 Only VIP users can use this command.")
