# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# Rewritten with Clean Architecture
# ==========================================

"""
Character Display Service

Handles sending random characters for the guess game with:
- Weighted rarity selection
- Image/Video display
- Auto-deletion after timeout
- Session tracking
"""

import asyncio
import logging
import random
import time
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field

from aiogram import Bot
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo
from aiogram.exceptions import TelegramBadRequest

from app.core.config import Config
from app.database.repositories.character import CharacterRepository
from app.database.models.character import Character
from app.services.cache import AsyncCache

logger = logging.getLogger(__name__)


@dataclass
class RarityConfig:
    """
    Configuration for a rarity tier.
    """
    weight: float
    enabled: bool = True
    emoji: str = ""
    display_name: str = ""


class RarityManager:
    """
    Manages rarity definitions and weights.
    """
    
    # Rarity definitions with weights
    RARITIES = {
        "Common": RarityConfig(weight=35, enabled=True, emoji="⚪️"),
        "Rare": RarityConfig(weight=20, enabled=True, emoji="🟣"),
        "Medium": RarityConfig(weight=15, enabled=True, emoji="🟢"),
        "Legendary": RarityConfig(weight=12, enabled=True, emoji="🟡"),
        "Special Edition": RarityConfig(weight=8, enabled=True, emoji="💮"),
        "Limited Edition": RarityConfig(weight=6, enabled=True, emoji="🔮"),
        "Premium": RarityConfig(weight=4, enabled=True, emoji="💸"),
        "Summer": RarityConfig(weight=3, enabled=False, emoji="🌤"),
        "Enchanted": RarityConfig(weight=2.5, enabled=True, emoji="🎐"),
        "Frozen": RarityConfig(weight=2, enabled=False, emoji="❄️"),
        "Romantic": RarityConfig(weight=2, enabled=False, emoji="💝"),
        "Haunted": RarityConfig(weight=1.8, enabled=False, emoji="🎃"),
        "Christmas": RarityConfig(weight=1.5, enabled=False, emoji="🎄"),
        "Festive": RarityConfig(weight=1.2, enabled=False, emoji="🧧"),
        "Naughty": RarityConfig(weight=1, enabled=True, emoji="🍑"),
        "AMV": RarityConfig(weight=0.8, enabled=False, emoji="🎗️"),
        "Cloudy": RarityConfig(weight=0.6, enabled=False, emoji="🌧"),
        "Mythgard": RarityConfig(weight=0.5, enabled=True, emoji="🦠"),
    }
    
    @classmethod
    def get_enabled_rarities(cls) -> List[str]:
        """
        Get all enabled rarity names.
        
        Returns:
            List of enabled rarity names
        """
        return [
            name for name, config in cls.RARITIES.items()
            if config.enabled
        ]
    
    @classmethod
    def get_weight(cls, rarity_name: str) -> float:
        """
        Get the weight for a rarity.
        
        Args:
            rarity_name: Name of the rarity
            
        Returns:
            Weight value (defaults to 0 if not found)
        """
        config = cls.RARITIES.get(rarity_name)
        return config.weight if config else 0
    
    @classmethod
    def get_emoji(cls, rarity_name: str) -> str:
        """
        Get the emoji for a rarity.
        
        Args:
            rarity_name: Name of the rarity
            
        Returns:
            Emoji string
        """
        config = cls.RARITIES.get(rarity_name)
        return config.emoji if config else "⭐"
    
    @classmethod
    def get_display_name(cls, rarity_name: str) -> str:
        """
        Get the display name for a rarity.
        
        Args:
            rarity_name: Name of the rarity
            
        Returns:
            Display name with emoji
        """
        config = cls.RARITIES.get(rarity_name)
        if config:
            return f"{config.emoji} {rarity_name}"
        return rarity_name


class CharacterDisplayService:
    """
    Service for displaying random characters for the guess game.
    """
    
    def __init__(
        self,
        character_repo: CharacterRepository,
        config: Config,
        delete_after_seconds: int = 300,
    ):
        """
        Initialize the character display service.
        
        Args:
            character_repo: Character repository
            config: Bot configuration
            delete_after_seconds: Seconds before auto-deletion
        """
        self.character_repo = character_repo
        self.config = config
        self.delete_after_seconds = delete_after_seconds
        
        # Session tracking
        self._last_characters: Dict[int, Dict] = {}
        self._first_correct_guesses: Dict[int, int] = {}
        self._sent_messages: Dict[int, List[int]] = {}
        
        # Cache for characters
        self._cache = AsyncCache(default_ttl=60)
        self._character_cache_key = "available_characters"
    
    # ===== Character Selection =====
    
    async def get_available_characters(self) -> List[Character]:
        """
        Get all available characters with enabled rarities.
        
        Returns:
            List of Character objects
        """
        # Check cache
        cached = await self._cache.get(self._character_cache_key)
        if cached is not None:
            return cached
        
        # Fetch from database
        enabled_rarities = RarityManager.get_enabled_rarities()
        all_characters = await self.character_repo.get_all()
        
        # Filter by enabled rarities
        available = [
            char for char in all_characters
            if char.rarity_name in enabled_rarities
        ]
        
        # Cache the results
        await self._cache.set(self._character_cache_key, available)
        logger.debug(f"Cached {len(available)} available characters")
        
        return available
    
    async def get_random_character(self) -> Optional[Character]:
        """
        Get a random character with weighted rarity selection.
        
        Returns:
            Selected Character or None if no characters available
        """
        available = await self.get_available_characters()
        
        if not available:
            logger.warning("No available characters found")
            return None
        
        # Build weighted selection list
        weighted_characters = []
        for character in available:
            weight = RarityManager.get_weight(character.rarity_name)
            if weight > 0:
                weighted_characters.append((character, weight))
        
        if not weighted_characters:
            # Fallback: pick random
            return random.choice(available)
        
        # Weighted random selection
        total_weight = sum(weight for _, weight in weighted_characters)
        rand = random.uniform(0, total_weight)
        
        cumulative = 0
        for character, weight in weighted_characters:
            cumulative += weight
            if rand <= cumulative:
                return character
        
        # Fallback
        return weighted_characters[-1][0]
    
    # ===== Message Sending =====
    
    async def send_character(
        self,
        bot: Bot,
        chat_id: int,
        character: Character,
        caption: Optional[str] = None,
    ) -> Optional[Message]:
        """
        Send a character as a photo or video.
        
        Args:
            bot: Bot instance
            chat_id: Target chat ID
            character: Character to send
            caption: Optional custom caption
            
        Returns:
            Sent message if successful, None otherwise
        """
        if not character:
            return None
        
        # Build caption
        if not caption:
            rarity_display = RarityManager.get_display_name(character.rarity_name)
            caption = (
                f"✨ A {rarity_display} Character Appears! ✨\n"
                f"🔍 Use /guess to claim this mysterious character!\n"
                f"💫 Hurry, before someone else snatches them!"
            )
        
        try:
            # Send as video if available
            if character.video_url:
                message = await bot.send_video(
                    chat_id=chat_id,
                    video=character.video_url,
                    caption=caption,
                    parse_mode="HTML",
                )
            elif character.image_url:
                message = await bot.send_photo(
                    chat_id=chat_id,
                    photo=character.image_url,
                    caption=caption,
                    parse_mode="HTML",
                )
            else:
                # No media available
                message = await bot.send_message(
                    chat_id=chat_id,
                    text=f"✨ {character.name} appears!\n{caption}",
                    parse_mode="HTML",
                )
            
            # Track the sent message
            self._track_message(chat_id, message.message_id)
            
            # Store as last character for this chat
            self._last_characters[chat_id] = {
                "character": character,
                "timestamp": time.time(),
            }
            
            # Clear first correct guess for this chat
            if chat_id in self._first_correct_guesses:
                del self._first_correct_guesses[chat_id]
            
            # Schedule deletion
            asyncio.create_task(
                self._schedule_deletion(bot, chat_id, message.message_id)
            )
            
            return message
            
        except Exception as e:
            logger.error(f"Failed to send character to {chat_id}: {e}")
            return None
    
    async def refresh_character(self, bot: Bot, chat_id: int) -> Optional[Message]:
        """
        Send a random character to a chat.
        
        Args:
            bot: Bot instance
            chat_id: Target chat ID
            
        Returns:
            Sent message if successful, None otherwise
        """
        character = await self.get_random_character()
        if not character:
            return None
        
        return await self.send_character(bot, chat_id, character)
    
    # ===== Message Tracking =====
    
    def _track_message(self, chat_id: int, message_id: int) -> None:
        """
        Track a sent message for cleanup.
        
        Args:
            chat_id: Chat ID
            message_id: Message ID
        """
        if chat_id not in self._sent_messages:
            self._sent_messages[chat_id] = []
        self._sent_messages[chat_id].append(message_id)
        
        # Limit tracked messages per chat
        if len(self._sent_messages[chat_id]) > 50:
            self._sent_messages[chat_id] = self._sent_messages[chat_id][-50:]
    
    async def _schedule_deletion(
        self,
        bot: Bot,
        chat_id: int,
        message_id: int
    ) -> None:
        """
        Schedule a message for deletion after the timeout.
        
        Args:
            bot: Bot instance
            chat_id: Chat ID
            message_id: Message ID
        """
        await asyncio.sleep(self.delete_after_seconds)
        try:
            await bot.delete_message(chat_id, message_id)
            logger.debug(f"Deleted message {message_id} in {chat_id}")
        except Exception as e:
            # Message might already be deleted or inaccessible
            logger.debug(f"Could not delete message {message_id}: {e}")
    
    # ===== Session Management =====
    
    def get_last_character(self, chat_id: int) -> Optional[Character]:
        """
        Get the last character sent to a chat.
        
        Args:
            chat_id: Chat ID
            
        Returns:
            Character if found, None otherwise
        """
        data = self._last_characters.get(chat_id)
        if data:
            # Check if still valid (5 minute timeout)
            if time.time() - data.get("timestamp", 0) < self.delete_after_seconds:
                return data.get("character")
        return None
    
    def get_first_correct_guess(self, chat_id: int) -> Optional[int]:
        """
        Get the user ID of the first correct guess for a chat.
        
        Args:
            chat_id: Chat ID
            
        Returns:
            User ID if set, None otherwise
        """
        return self._first_correct_guesses.get(chat_id)
    
    def set_first_correct_guess(self, chat_id: int, user_id: int) -> None:
        """
        Set the first correct guess for a chat.
        
        Args:
            chat_id: Chat ID
            user_id: User ID of the first correct guess
        """
        if chat_id not in self._first_correct_guesses:
            self._first_correct_guesses[chat_id] = user_id
    
    def clear_session(self, chat_id: int) -> None:
        """
        Clear all session data for a chat.
        
        Args:
            chat_id: Chat ID
        """
        if chat_id in self._last_characters:
            del self._last_characters[chat_id]
        if chat_id in self._first_correct_guesses:
            del self._first_correct_guesses[chat_id]
        if chat_id in self._sent_messages:
            del self._sent_messages[chat_id]
    
    # ===== Cache Management =====
    
    async def refresh_cache(self) -> None:
        """
        Refresh the character cache.
        """
        await self._cache.delete(self._character_cache_key)
        await self.get_available_characters()
        logger.info("Character cache refreshed")
    
    async def clear_all_sessions(self) -> None:
        """
        Clear all session data.
        """
        self._last_characters.clear()
        self._first_correct_guesses.clear()
        self._sent_messages.clear()
        logger.info("All sessions cleared")


# ===== Factory Function =====

def create_character_display_service(config: Config) -> CharacterDisplayService:
    """
    Create a character display service instance.
    
    Args:
        config: Bot configuration
        
    Returns:
        CharacterDisplayService instance
    """
    from app.database.manager import get_db_manager
    from app.database.repositories.character import CharacterRepository
    
    db_manager = get_db_manager()
    character_repo = CharacterRepository(db_manager)
    
    delete_after = config.CHARACTER_DISPLAY_TIMEOUT or 300
    
    return CharacterDisplayService(
        character_repo=character_repo,
        config=config,
        delete_after_seconds=delete_after,
    )


# ===== Backward Compatibility =====

class LegacyDisplayCompat:
    """
    Backward compatibility wrapper for old send_image functions.
    """
    
    def __init__(self):
        self._service: Optional[CharacterDisplayService] = None
    
    @property
    def service(self) -> CharacterDisplayService:
        if self._service is None:
            from app.core.config import get_config
            config = get_config()
            self._service = create_character_display_service(config)
        return self._service
    
    async def send_image(self, bot, chat_id: int) -> Optional[Message]:
        """
        Legacy send_image function.
        """
        return await self.service.refresh_character(bot, chat_id)
    
    async def send_character(self, bot, chat_id: int, character_data: Dict) -> Optional[Message]:
        """
        Legacy send_character function.
        """
        from app.database.models.character import Character
        
        character = Character.from_dict(character_data)
        return await self.service.send_character(bot, chat_id, character)
    
    def get_last_character(self, chat_id: int) -> Optional[Dict]:
        """
        Legacy get_last_character function.
        """
        character = self.service.get_last_character(chat_id)
        if character:
            return character.to_dict()
        return None
    
    def get_first_correct_guess(self, chat_id: int) -> Optional[int]:
        """
        Legacy get_first_correct_guess function.
        """
        return self.service.get_first_correct_guess(chat_id)
    
    def set_first_correct_guess(self, chat_id: int, user_id: int) -> None:
        """
        Legacy set_first_correct_guess function.
        """
        self.service.set_first_correct_guess(chat_id, user_id)


# For backward compatibility
legacy_display = LegacyDisplayCompat()

# Old functions
send_image = legacy_display.send_image
get_last_character = legacy_display.get_last_character
get_first_correct_guess = legacy_display.get_first_correct_guess
set_first_correct_guess = legacy_display.set_first_correct_guess
