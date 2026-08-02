# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# Rewritten with Clean Architecture
# ==========================================

"""
TEAMZYRO Package - Waifu Bot

This package contains all bot modules organized by functionality.
"""

import logging
from typing import Optional

# Package version
__version__ = "2.0.0"
__author__ = "MrZyro"
__repo__ = "https://github.com/MrZyro"

# Configure package logger
logger = logging.getLogger(__name__)

# Export main components
from app.core.config import Config, get_config
from app.database.manager import DatabaseManager
from app.bot import create_bot, create_dispatcher

# Package exports
__all__ = [
    "Config",
    "get_config",
    "DatabaseManager",
    "create_bot",
    "create_dispatcher",
    "__version__",
    "__author__",
    "__repo__",
]

# Lazy imports for backward compatibility
# This allows old code to still work with `from TEAMZYRO import *`
class _LazyModule:
    """Lazy loader for backward compatibility with old import patterns."""
    
    def __init__(self):
        self._modules = {}
    
    def __getattr__(self, name):
        # Don't intercept special attributes
        if name.startswith("_"):
            raise AttributeError(f"'{name}' not found")
        
        # Map old module names to new locations
        module_map = {
            # Old import -> New location
            "LOGGER": "app.core.logging.get_logger",
            "ZYRO": "app.bot.create_bot",
            "application": "app.bot.create_application",
            "bot": "app.bot.create_bot",
            "dp": "app.bot.create_dispatcher",
            "collection": "app.database.repositories.character",
            "user_collection": "app.database.repositories.user",
            "user_totals_collection": "app.database.repositories.stats",
            "group_user_totals_collection": "app.database.repositories.group_stats",
            "top_global_groups_collection": "app.database.repositories.top_groups",
            "pm_users": "app.database.repositories.pm_users",
            "discounts_collection": "app.database.repositories.discounts",
            "redeem_collection": "app.database.repositories.redeem",
        }
        
        if name in module_map:
            new_path = module_map[name]
            logger.warning(f"⚠️ Deprecated import: 'from TEAMZYRO import {name}' "
                          f"→ Use 'from {new_path}' instead")
            return self._import_module(new_path)
        
        # If not in map, raise error
        raise AttributeError(
            f"'{name}' is not a valid import from TEAMZYRO. "
            f"Please check the new module structure."
        )
    
    def _import_module(self, path):
        """Import a module dynamically."""
        if path in self._modules:
            return self._modules[path]
        
        parts = path.split('.')
        module_name = '.'.join(parts[:-1])
        attr_name = parts[-1]
        
        try:
            module = __import__(module_name, fromlist=[attr_name])
            obj = getattr(module, attr_name)
            self._modules[path] = obj
            return obj
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to import {path}: {e}")
            return None


# Allow `from TEAMZYRO import *` to work with deprecation warnings
import sys
sys.modules[__name__] = _LazyModule()


# Clean package initialization
def init_package() -> None:
    """
    Initialize the TEAMZYRO package.
    This is called when the package is first imported.
    """
    # Configure logging for the package
    logging.getLogger(__name__).info("🦋 TEAMZYRO Package initialized (v2.0.0)")
