# ==========================================
# Handlers Package (Updated)
# ==========================================

"""
All handler routers organized by category.
"""

from aiogram import Dispatcher

from app.handlers.user.start import router as start_router
from app.handlers.user.help import router as help_router
from app.handlers.user.profile import router as profile_router
from app.handlers.user.balance import router as balance_router
from app.handlers.admin import ADMIN_ROUTERS
from app.handlers.game import GAME_ROUTERS
from app.handlers.economy import ECONOMY_ROUTERS


def register_all_routers(dp: Dispatcher) -> None:
    """
    Register all handler routers with the dispatcher.
    
    Args:
        dp: Aiogram dispatcher
    """
    # User routers
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(profile_router)
    dp.include_router(balance_router)
    
    # Admin routers
    for router in ADMIN_ROUTERS:
        dp.include_router(router)
    
    # Game routers
    for router in GAME_ROUTERS:
        dp.include_router(router)
    
    # Economy routers
    for router in ECONOMY_ROUTERS:
        dp.include_router(router)
    
    # Callback routers
    from app.callbacks import CALLBACK_ROUTERS
    for router in CALLBACK_ROUTERS:
        dp.include_router(router)
    
    logger.info("✅ All routers registered")
