# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Help System Package

Provides structured help data for all bot commands and features.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field

from app.assets.help.user import USER_HELP
from app.assets.help.economy import ECONOMY_HELP
from app.assets.help.games import GAMES_HELP
from app.assets.help.admin import ADMIN_HELP
from app.assets.help.utils import UTILS_HELP


@dataclass
class HelpEntry:
    """
    A single help entry for a command or feature.
    """
    name: str
    display_name: str
    description: str
    usage: Optional[str] = None
    examples: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    
    def format(self, bot_username: str = "") -> str:
        """
        Format the help entry as a string.
        
        Args:
            bot_username: Bot username for inline examples
            
        Returns:
            Formatted help text
        """
        lines = []
        
        # Title
        lines.append(f"{self.display_name}")
        lines.append("━" * 40)
        lines.append("")
        
        # Description
        if self.description:
            lines.append(self.description)
            lines.append("")
        
        # Usage
        if self.usage:
            lines.append(f"📝 **Usage:**")
            lines.append(f"`{self.usage}`")
            lines.append("")
        
        # Examples
        if self.examples:
            lines.append(f"📌 **Examples:**")
            for example in self.examples:
                # Replace bot username placeholder
                if bot_username:
                    example = example.replace("{BOT_USERNAME}", bot_username)
                lines.append(f"• {example}")
            lines.append("")
        
        # Notes
        if self.notes:
            lines.append(f"⚠️ **Notes:**")
            for note in self.notes:
                lines.append(f"• {note}")
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, str]:
        """
        Convert to dictionary format for backward compatibility.
        
        Returns:
            Dictionary with HELP_NAME and HELP keys
        """
        return {
            "HELP_NAME": self.display_name,
            "HELP": self.format()
        }


def get_all_help_entries() -> Dict[str, HelpEntry]:
    """
    Get all help entries across all categories.
    
    Returns:
        Dictionary mapping command names to HelpEntry objects
    """
    all_entries = {}
    
    # Merge all help dictionaries
    help_sources = [
        USER_HELP,
        ECONOMY_HELP,
        GAMES_HELP,
        ADMIN_HELP,
        UTILS_HELP,
    ]
    
    for source in help_sources:
        for key, entry in source.items():
            if key not in all_entries:
                all_entries[key] = entry
            else:
                # Duplicate key - log warning but keep existing
                import logging
                logging.warning(f"Duplicate help key: {key}")
    
    return all_entries


def get_help_data(bot_username: str = "") -> Dict[str, Dict[str, str]]:
    """
    Get help data in the legacy format for backward compatibility.
    
    Args:
        bot_username: Bot username for formatting
        
    Returns:
        Dictionary in the old HELP_DATA format
    """
    entries = get_all_help_entries()
    result = {}
    
    for key, entry in entries.items():
        result[key] = {
            "HELP_NAME": entry.display_name,
            "HELP": entry.format(bot_username)
        }
    
    return result


# Export for backward compatibility
HELP_DATA = get_help_data()


__all__ = [
    "HelpEntry",
    "get_all_help_entries",
    "get_help_data",
    "HELP_DATA",
  ]
