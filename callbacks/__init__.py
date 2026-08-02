from aiogram import Dispatcher

from callbacks.help import router as help_router
from callbacks.harem import router as harem_router
from callbacks.check import router as check_router
from callbacks.search import router as search_router
from callbacks.gift import router as gift_router
from callbacks.tictactoe import router as tictactoe_router
from callbacks.mines import router as mines_router
from callbacks.shop import router as shop_router
from callbacks.sudo import router as sudo_router


def register_all_callbacks(dp: Dispatcher):
    """Register all callback handlers."""
    dp.include_router(help_router)
    dp.include_router(harem_router)
    dp.include_router(check_router)
    dp.include_router(search_router)
    dp.include_router(gift_router)
    dp.include_router(tictactoe_router)
    dp.include_router(mines_router)
    dp.include_router(shop_router)
    dp.include_router(sudo_router)
