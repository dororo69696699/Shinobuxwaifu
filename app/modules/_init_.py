# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# Rewritten with Clean Architecture
# ==========================================

"""
Handler Registration Module

This module handles the registration of all bot handlers, including:
- User commands
- Admin commands
- Game commands
- Economy commands
- Callback handlers
"""

import logging
import time
from typing import List, Optional, Type

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from app.core.config import Config
from app.filters.admin import AdminFilter
from app.filters.chat_type import ChatTypeFilter

# Package metadata
__version__ = "2.0.0"
__author__ = "MrZyro"
__repo__ = "https://github.com/MrZyro"

# Start time for uptime tracking
START_TIME: float = time.time()

# Configure logger
logger = logging.getLogger(__name__)

# Module discovery and registration
class HandlerRegistry:
    """
    Centralized handler registry for managing all bot handlers.
    Handles automatic discovery and registration of handlers.
    """
    
    def __init__(self, dp: Dispatcher, config: Config):
        """
        Initialize the handler registry.
        
        Args:
            dp: Aiogram dispatcher instance
            config: Bot configuration
        """
        self.dp = dp
        self.config = config
        self._handlers: List[dict] = []
        self._registered: List[str] = []
    
    def register_all(self) -> None:
        """
        Register all handlers in the correct order.
        This is the main entry point for handler registration.
        """
        logger.info("🔄 Registering handlers...")
        
        # Register in order of priority
        self._register_admin_handlers()
        self._register_user_handlers()
        self._register_game_handlers()
        self._register_economy_handlers()
        self._register_callback_handlers()
        self._register_error_handlers()
        
        logger.info(f"✅ Registered {len(self._registered)} handler modules")
    
    def _register_admin_handlers(self) -> None:
        """Register admin-only command handlers."""
        from app.handlers.admin import (
            broadcast,
            stats,
            ban,
            unban,
            set_waifu,
            delete_waifu,
            redeem_code,
            give_coins,
            reset_stats,
            backup,
            restore_backup,
        )
        
        admin_filters = [AdminFilter(self.config.OWNER_ID)]
        
        handlers = [
            (broadcast, "broadcast"),
            (stats, "stats"),
            (ban, "ban"),
            (unban, "unban"),
            (set_waifu, "setwaifu"),
            (delete_waifu, "delwaifu"),
            (redeem_code, "createredeem"),
            (give_coins, "givecoins"),
            (reset_stats, "resetstats"),
            (backup, "backup"),
            (restore_backup, "restorebackup"),
        ]
        
        for handler, name in handlers:
            self._register_handler(handler, admin_filters, name)
    
    def _register_user_handlers(self) -> None:
        """Register standard user command handlers."""
        from app.handlers.user import (
            start,
            help_command,
            profile,
            daily,
            balance,
            inventory,
            waifu_list,
            waifu_details,
            marry,
            divorce,
            trade,
        )
        
        handlers = [
            (start, "start"),
            (help_command, "help"),
            (profile, "profile"),
            (daily, "daily"),
            (balance, "balance"),
            (inventory, "inventory"),
            (waifu_list, "waifus"),
            (waifu_details, "waifu"),
            (marry, "marry"),
            (divorce, "divorce"),
            (trade, "trade"),
        ]
        
        for handler, name in handlers:
            self._register_handler(handler, [], name)
    
    def _register_game_handlers(self) -> None:
        """Register game command handlers."""
        from app.handlers.game import (
            gacha,
            guess_waifu,
            blackjack,
            minesweeper,
            chess,
            tictactoe,
            leaderboard,
            daily_challenge,
        )
        
        handlers = [
            (gacha, "gacha"),
            (guess_waifu, "guess"),
            (blackjack, "blackjack"),
            (minesweeper, "mines"),
            (chess, "chess"),
            (tictactoe, "tictactoe"),
            (leaderboard, "leaderboard"),
            (daily_challenge, "challenge"),
        ]
        
        for handler, name in handlers:
            self._register_handler(handler, [], name)
    
    def _register_economy_handlers(self) -> None:
        """Register economy and shop command handlers."""
        from app.handlers.economy import (
            shop,
            buy,
            sell,
            gift,
            redeem,
            quests,
            weekly,
            vote,
        )
        
        handlers = [
            (shop, "shop"),
            (buy, "buy"),
            (sell, "sell"),
            (gift, "gift"),
            (redeem, "redeem"),
            (quests, "quests"),
            (weekly, "weekly"),
            (vote, "vote"),
        ]
        
        for handler, name in handlers:
            self._register_handler(handler, [], name)
    
    def _register_callback_handlers(self) -> None:
        """Register callback query handlers."""
        from app.callbacks import (
            handle_pagination,
            handle_shop_purchase,
            handle_game_move,
            handle_card_select,
            handle_marriage_accept,
            handle_trade_accept,
        )
        
        callbacks = [
            handle_pagination,
            handle_shop_purchase,
            handle_game_move,
            handle_card_select,
            handle_marriage_accept,
            handle_trade_accept,
        ]
        
        for callback in callbacks:
            self.dp.callback_query.register(callback)
            self._registered.append(callback.__name__)
            logger.debug(f"  📞 Registered callback: {callback.__name__}")
    
    def _register_error_handlers(self) -> None:
        """Register error handlers."""
        from app.middleware.error_handler import ErrorHandlerMiddleware
        
        # Register error middleware
        self.dp.message.middleware(ErrorHandlerMiddleware())
        self.dp.callback_query.middleware(ErrorHandlerMiddleware())
        self._registered.append("ErrorHandlerMiddleware")
        logger.debug("  ✅ Registered error handlers")
    
    def _register_handler(
        self,
        handler: callable,
        filters: List,
        name: str
    ) -> None:
        """
        Register a single handler with the dispatcher.
        
        Args:
            handler: The handler function
            filters: List of filters to apply
            name: Handler name for logging
        """
        # Build filter chain
        filter_chain = filters.copy()
        
        # Add default filters
        filter_chain.append(ChatTypeFilter(["private", "group", "supergroup"]))
        
        # Register the handler
        self.dp.message.register(handler, *filter_chain)
        self._registered.append(name)
        logger.debug(f"  ✅ Registered handler: {name}")


def register_all_handlers(dp: Dispatcher, config: Config) -> None:
    """
    Register all handlers for the bot.
    This is the main entry point for handler registration.
    
    Args:
        dp: Aiogram dispatcher instance
        config: Bot configuration
    """
    registry = HandlerRegistry(dp, config)
    registry.register_all()
    logger.info(f"🎯 All handlers registered successfully")


def get_handlers_list() -> List[str]:
    """
    Get a list of all available handler modules.
    This is used for debugging and documentation.
    
    Returns:
        List of handler module names
    """
    handler_modules = [
        "admin",
        "user",
        "game",
        "economy",
    ]
    return handler_modules


def get_start_time() -> float:
    """
    Get the bot start time.
    
    Returns:
        Unix timestamp of bot start
    """
    return START_TIME


def get_uptime() -> float:
    """
    Get the bot uptime in seconds.
    
    Returns:
        Uptime in seconds
    """
    return time.time() - START_TIME


# Backward compatibility for old module loading
# This allows old code that used ALL_MODULES to still work
class _ModuleList:
    """Lazy module list for backward compatibility."""
    
    def __init__(self):
        self._modules = None
    
    def __call__(self):
        if self._modules is None:
            self._modules = get_handlers_list()
        return self._modules
    
    def __iter__(self):
        return iter(self())


# Export for backward compatibility
ALL_MODULES = _ModuleList()

# Package exports
__all__ = [
    "register_all_handlers",
    "get_handlers_list",
    "get_start_time",
    "get_uptime",
    "ALL_MODULES",
]
