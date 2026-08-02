# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Search Callbacks - Pagination
"""

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode

from modules.search import handle_search

router = Router(name="search_callbacks")


@router.callback_query(lambda c: c.data.startswith("sips:"))
async def search_callback(callback: CallbackQuery) -> None:
    """Handle search pagination."""
    data = callback.data.split(":")
    query = data[1]
    page = int(data[2])
    
    await callback.answer()
    await handle_search(callback.message, query, page, is_callback=True)
