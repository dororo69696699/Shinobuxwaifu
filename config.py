

"""
Configuration management for the Waifu Bot.
Loads environment variables and provides a centralized config object.
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional, Union

from dotenv import load_dotenv


@dataclass
class Config:
    """
    Centralized configuration for the bot.
    All settings are loaded from environment variables with validation.
    """
    
    # ===== Telegram API =====
    BOT_TOKEN: str = field(default_factory=lambda: os.getenv("BOT_TOKEN", ""))
    API_ID: str = field(default_factory=lambda: os.getenv("API_ID", ""))
    API_HASH: str = field(default_factory=lambda: os.getenv("API_HASH", ""))
    
    # ===== Database =====
    MONGO_URI: str = field(default_factory=lambda: os.getenv("MONGO_URI", ""))
    BACKUP_MONGO_URI: str = field(default_factory=lambda: os.getenv("BACKUP_MONGO_URI", ""))
    DB_NAME: str = field(default_factory=lambda: os.getenv("DB_NAME", "WAIFUBOT"))
    
    # ===== Channels & Chats =====
    FORCE_JOIN: str = field(default_factory=lambda: os.getenv("FORCE_JOIN", ""))
    BOT_LOGGING: str = field(default_factory=lambda: os.getenv("BOT_LOGGING", ""))
    SUPPORT_CHAT: str = field(default_factory=lambda: os.getenv("SUPPORT_CHAT", ""))
    UPDATE_CHAT: str = field(default_factory=lambda: os.getenv("UPDATE_CHAT", ""))
    MUSIC_JOIN: str = field(default_factory=lambda: os.getenv("MUSIC_JOIN", ""))
    CHARA_CHANNEL_ID: int = int(os.getenv("CHARA_CHANNEL_ID", "-1004305990907"))
    
    # ===== Admin =====
    OWNER_ID: int = field(default_factory=lambda: int(os.getenv("OWNER_ID", "0")))
    
    # ===== APIs =====
    IMGBB_API_KEY: str = field(default_factory=lambda: os.getenv("IMGBB_API_KEY", ""))
    
    # ===== Media =====
    START_MEDIA: List[str] = field(default_factory=lambda: [
        os.getenv("START_MEDIA_1", "https://files.catbox.moe/5zrb1a.mp4"),
        os.getenv("START_MEDIA_2", "https://files.catbox.moe/5zrb1a.mp4")
    ])
    
    PHOTO_URL: List[str] = field(default_factory=lambda: [
        os.getenv("PHOTO_URL_1", "https://i.ibb.co/v6H9qNn7/file-0000000099dc71f5a902afba055b1567.png"),
        os.getenv("PHOTO_URL_2", "https://i.ibb.co/v6H9qNn7/file-0000000099dc71f5a902afba055b1567.png")
    ])
    
    STATS_IMG: str = field(default_factory=lambda: os.getenv("STATS_IMG", "https://files.catbox.moe/gknnju.jpg"))
    
    # ===== Bot Settings =====
    BOT_USERNAME: Optional[str] = None
    BOT_ID: Optional[int] = None
    FORCE_JOIN_LINK: Optional[str] = None
    
    # Internal references (set during runtime)
    bot: Optional['Bot'] = None
    dispatcher: Optional['Dispatcher'] = None
    db_manager: Optional['DatabaseManager'] = None
    
    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """
        Validate required configuration values.
        
        Raises:
            ValueError: If required values are missing or invalid.
        """
        # Required: Token
        if not self.BOT_TOKEN:
            raise ValueError(
                "❌ BOT_TOKEN is required!\n"
                "Please set it in your .env file or environment variables."
            )
        
        # Required: Database
        if not self.MONGO_URI:
            raise ValueError(
                "❌ MONGO_URI is required!\n"
                "Please set it in your .env file or environment variables."
            )
        
        # Required: Force Join channel
        if not self.FORCE_JOIN:
            raise ValueError(
                "❌ FORCE_JOIN is required!\n"
                "Please set it in your .env file or environment variables."
            )
        
        # Required: Logging channel
        if not self.BOT_LOGGING:
            raise ValueError(
                "❌ BOT_LOGGING is required!\n"
                "Please set it in your .env file or environment variables."
            )
        
        # Validate Owner ID
        if self.OWNER_ID == 0:
            raise ValueError(
                "❌ OWNER_ID is required and must be a valid Telegram User ID!\n"
                "Please set it in your .env file or environment variables."
            )
        
        # Validate numeric fields
        try:
            if self.FORCE_JOIN:
                # Can be username or ID
                pass
        except ValueError:
            raise ValueError(f"❌ FORCE_JOIN must be a valid channel ID or username: {self.FORCE_JOIN}")
        
        try:
            if self.BOT_LOGGING:
                # Can be username or ID
                pass
        except ValueError:
            raise ValueError(f"❌ BOT_LOGGING must be a valid chat ID or username: {self.BOT_LOGGING}")
    
    def is_owner(self, user_id: int) -> bool:
        """
        Check if a user is the bot owner.
        
        Args:
            user_id: Telegram user ID to check
            
        Returns:
            True if user is owner, False otherwise
        """
        return user_id == self.OWNER_ID
    
    def is_admin(self, user_id: int) -> bool:
        """
        Check if a user is an admin (currently only owner).
        Extend this later for admin lists.
        
        Args:
            user_id: Telegram user ID to check
            
        Returns:
            True if user is admin, False otherwise
        """
        return self.is_owner(user_id)
    
    def get_force_join_target(self) -> Union[int, str]:
        """
        Get the force join channel target.
        
        Returns:
            Channel ID as int or username as str
        """
        try:
            return int(self.FORCE_JOIN)
        except ValueError:
            return self.FORCE_JOIN
    
    def get_logging_target(self) -> Union[int, str]:
        """
        Get the logging channel target.
        
        Returns:
            Chat ID as int or username as str
        """
        try:
            return int(self.BOT_LOGGING)
        except ValueError:
            return self.BOT_LOGGING


# For backward compatibility, create a singleton instance
# This allows existing code that imports config.py to work
def get_config() -> Config:
    """
    Get the global config instance.
    Creates it if it doesn't exist.
    
    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


# Global config instance (lazy-loaded)
_config: Optional[Config] = None


# Legacy compatibility variables (to ease transition)
# These will be deprecated and removed in future versions
def __getattr__(name: str):
    """
    Provide backward compatibility for old global variable access.
    
    Args:
        name: Name of the attribute to get
        
    Returns:
        The attribute value from the config instance
        
    Raises:
        AttributeError: If the attribute doesn't exist
    """
    if name.startswith('_'):
        raise AttributeError(f"'{name}' not found")
    
    config = get_config()
    if hasattr(config, name):
        return getattr(config, name)
    
    raise AttributeError(f"'{name}' not found in config")


# Cleanup to avoid polluting the namespace
__all__ = [
    'Config',
    'get_config',
  ]

# Add to the Config dataclass:

# ===== Notifications =====
STARTUP_IMAGE: str = field(
    default_factory=lambda: os.getenv("STARTUP_IMAGE", "https://files.catbox.moe/ehv507.jpeg")
)
OWNER_DISPLAY_NAME: str = field(
    default_factory=lambda: os.getenv("OWNER_DISPLAY_NAME", "")
)

# ===== Bot Username =====
BOT_USERNAME: Optional[str] = field(
    default_factory=lambda: os.getenv("BOT_USERNAME", "")
)

# Add to the Config dataclass:

# ===== Inline Search =====
INLINE_CACHE_TTL: int = int(os.getenv("INLINE_CACHE_TTL", "300"))
USER_CACHE_TTL: int = int(os.getenv("USER_CACHE_TTL", "30"))
SEARCH_CACHE_TTL: int = int(os.getenv("SEARCH_CACHE_TTL", "60"))
