
# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# Rewritten with Clean Architecture
# ==========================================

"""
Reaction Service Module

Handles adding reactions (emoji) to messages with:
- Random emoji selection
- Aiogram's built-in reaction methods
- Rate limiting protection
- Error handling and retries
- Configurable emoji list
"""

import asyncio
import logging
import random
from typing import List, Optional, Union

from aiogram import Bot
from aiogram.types import ReactionTypeEmoji, Message
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramRetryAfter,
)

from app.core.config import Config

logger = logging.getLogger(__name__)


class ReactionService:
    """
    Service for adding reactions to messages.
    """
    
    # Default emojis available for reactions
    DEFAULT_EMOJIS = [
        "👍", "😘", "❤️", "🔥", "🥰", "🤩", "💘", 
        "😏", "🤯", "⚡️", "🏆", "🤭", "🎉", "💖",
        "✨", "🌟", "💎", "🌸", "🎀", "💫", "🌈",
    ]
    
    def __init__(
        self,
        config: Config,
        emojis: Optional[List[str]] = None,
        enabled: bool = True,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initialize the reaction service.
        
        Args:
            config: Bot configuration
            emojis: List of emojis to choose from
            enabled: Whether reactions are enabled
            max_retries: Maximum retry attempts on failure
            retry_delay: Delay between retries in seconds
        """
        self.config = config
        self.emojis = emojis or self.DEFAULT_EMOJIS
        self.enabled = enabled
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Track recently reacted messages to avoid spam
        self._recent_messages: set = set()
        self._cleanup_task: Optional[asyncio.Task] = None
    
    async def react_to_message(
        self,
        bot: Bot,
        chat_id: Union[int, str],
        message_id: int,
        emoji: Optional[str] = None,
        force: bool = False,
    ) -> bool:
        """
        Add a reaction to a message.
        
        Args:
            bot: Bot instance
            chat_id: Chat ID or username
            message_id: Message ID to react to
            emoji: Optional specific emoji (random if not provided)
            force: Force reaction even if recently reacted
            
        Returns:
            True if reaction was added, False otherwise
        """
        # Check if reactions are enabled
        if not self.enabled:
            logger.debug("Reactions are disabled")
            return False
        
        # Check for spam (recently reacted to this message)
        message_key = f"{chat_id}:{message_id}"
        if not force and message_key in self._recent_messages:
            logger.debug(f"Skipping reaction to {message_key} (recently reacted)")
            return False
        
        # Select emoji
        selected_emoji = emoji or random.choice(self.emojis)
        
        # Add reaction with retries
        for attempt in range(self.max_retries):
            try:
                # Create reaction type
                reaction = ReactionTypeEmoji(emoji=selected_emoji)
                
                # Set reaction using Aiogram
                await bot.set_message_reaction(
                    chat_id=chat_id,
                    message_id=message_id,
                    reaction=[reaction],
                )
                
                # Track this message
                self._recent_messages.add(message_key)
                
                logger.debug(
                    f"✅ Added reaction '{selected_emoji}' to message {message_id} "
                    f"in chat {chat_id}"
                )
                return True
                
            except TelegramRetryAfter as e:
                # Rate limited - wait and retry
                wait_time = e.retry_after
                logger.warning(
                    f"Rate limited while reacting to {message_id}. "
                    f"Waiting {wait_time}s (attempt {attempt + 1}/{self.max_retries})"
                )
                await asyncio.sleep(wait_time)
                
            except TelegramForbiddenError:
                # Bot can't react (no permission)
                logger.warning(
                    f"Cannot react to message {message_id} in chat {chat_id}: "
                    "Bot doesn't have permission"
                )
                return False
                
            except TelegramBadRequest as e:
                # Invalid emoji or message
                logger.error(
                    f"Failed to react to message {message_id}: {e}"
                )
                return False
                
            except Exception as e:
                # Other errors
                logger.error(
                    f"Unexpected error reacting to message {message_id}: {e}"
                )
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    return False
        
        return False
    
    async def react_with_multiple(
        self,
        bot: Bot,
        chat_id: Union[int, str],
        message_id: int,
        emojis: List[str],
    ) -> bool:
        """
        React with multiple emojis at once.
        
        Args:
            bot: Bot instance
            chat_id: Chat ID or username
            message_id: Message ID
            emojis: List of emojis to add
            
        Returns:
            True if reactions were added, False otherwise
        """
        if not self.enabled or not emojis:
            return False
        
        try:
            reactions = [ReactionTypeEmoji(emoji=e) for e in emojis[:3]]  # Max 3 reactions
            
            await bot.set_message_reaction(
                chat_id=chat_id,
                message_id=message_id,
                reaction=reactions,
            )
            
            logger.debug(
                f"✅ Added {len(reactions)} reactions to message {message_id} "
                f"in chat {chat_id}"
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to add multiple reactions: {e}")
            return False
    
    async def clear_reactions(
        self,
        bot: Bot,
        chat_id: Union[int, str],
        message_id: int,
    ) -> bool:
        """
        Clear all reactions from a message.
        
        Args:
            bot: Bot instance
            chat_id: Chat ID or username
            message_id: Message ID
            
        Returns:
            True if reactions were cleared, False otherwise
        """
        try:
            await bot.set_message_reaction(
                chat_id=chat_id,
                message_id=message_id,
                reaction=[],  # Empty list clears all reactions
            )
            return True
        except Exception as e:
            logger.error(f"Failed to clear reactions: {e}")
            return False
    
    async def react_random_to_message(
        self,
        bot: Bot,
        chat_id: Union[int, str],
        message_id: int,
    ) -> bool:
        """
        React with a random emoji to a message.
        
        Args:
            bot: Bot instance
            chat_id: Chat ID or username
            message_id: Message ID
            
        Returns:
            True if reaction was added, False otherwise
        """
        return await self.react_to_message(bot, chat_id, message_id)
    
    # ===== Auto-Cleanup =====
    
    async def _cleanup_recent_messages(self) -> None:
        """
        Clean up the recent messages set periodically.
        """
        while True:
            await asyncio.sleep(60)  # Clean every minute
            # Keep only last 1000 messages
            if len(self._recent_messages) > 1000:
                # Convert to list and slice
                recent_list = list(self._recent_messages)
                self._recent_messages = set(recent_list[-1000:])
    
    def start_cleanup(self) -> None:
        """
        Start the background cleanup task.
        """
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_recent_messages())
    
    def stop_cleanup(self) -> None:
        """
        Stop the background cleanup task.
        """
        if self._cleanup_task:
            self._cleanup_task.cancel()
            self._cleanup_task = None
    
    # ===== Configuration =====
    
    def add_emojis(self, *emojis: str) -> None:
        """
        Add emojis to the available list.
        
        Args:
            emojis: Emojis to add
        """
        self.emojis.extend(emojis)
        # Remove duplicates while preserving order
        self.emojis = list(dict.fromkeys(self.emojis))
    
    def set_emojis(self, emojis: List[str]) -> None:
        """
        Set the complete emoji list.
        
        Args:
            emojis: New list of emojis
        """
        self.emojis = emojis
    
    def enable(self) -> None:
        """Enable reactions."""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable reactions."""
        self.enabled = False


# ===== Factory Function =====

def create_reaction_service(config: Config) -> ReactionService:
    """
    Create a reaction service instance.
    
    Args:
        config: Bot configuration
        
    Returns:
        ReactionService instance
    """
    # Get custom emojis from config if available
    emojis = None
    if hasattr(config, 'REACTION_EMOJIS') and config.REACTION_EMOJIS:
        emojis = config.REACTION_EMOJIS.split(',')
        emojis = [e.strip() for e in emojis if e.strip()]
    
    enabled = getattr(config, 'REACTIONS_ENABLED', True)
    
    return ReactionService(
        config=config,
        emojis=emojis,
        enabled=enabled,
    )


# ===== Backward Compatibility =====

class LegacyReactionCompat:
    """
    Backward compatibility wrapper for old reaction functions.
    """
    
    def __init__(self):
        self._service: Optional[ReactionService] = None
    
    @property
    def service(self) -> ReactionService:
        if self._service is None:
            from app.core.config import get_config
            config = get_config()
            self._service = create_reaction_service(config)
        return self._service
    
    async def react_to_message(self, chat_id: Union[int, str], message_id: int) -> bool:
        """
        Legacy react_to_message function.
        """
        from app.bot import get_bot
        bot = await get_bot()
        return await self.service.react_random_to_message(bot, chat_id, message_id)


# Create singleton for backward compatibility
legacy_react = LegacyReactionCompat()

# Old function
react_to_message = legacy_react.react_to_message

# Also export the emojis list for backward compatibility
emojis = ReactionService.DEFAULT_EMOJIS
