from aiogram import Dispatcher

from handlers.message import router as message_router
from handlers.inline import router as inline_router


def register_all_handlers(dp: Dispatcher):
    """Register all handler routers."""
    dp.include_router(message_router)
    dp.include_router(inline_router)
