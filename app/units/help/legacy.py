# ==========================================
# Legacy Help Data Compatibility
# ==========================================

"""
Provides the old HELP_DATA format for backward compatibility.
"""

from typing import Dict, Any

from app.assets.help import get_help_data
from app.core.config import get_config


def get_legacy_help_data() -> Dict[str, Any]:
    """
    Get help data in the old format.
    
    Returns:
        Dictionary in the old HELP_DATA format
    """
    config = get_config()
    bot_username = config.BOT_USERNAME or ""
    return get_help_data(bot_username)


# For direct import: from app.assets.help.legacy import HELP_DATA
HELP_DATA = get_legacy_help_data()


__all__ = ["HELP_DATA", "get_legacy_help_data"]
