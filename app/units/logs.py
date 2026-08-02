
# ==========================================

"""
Notification Service Module

Handles all bot notifications including:
- Startup messages
- Error alerts
- System status updates
- Channel announcements
"""

import logging
from typing import Optional, Union

from aiogram import Bot
from aiogram.types import InputMediaPhoto, Message

from app.core.config import Config
from app.services.template import TemplateService

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service for sending notifications to logging channels and users.
    """
    
    def __init__(self, config: Config, bot: Optional[Bot] = None):
        """
        Initialize the notification service.
        
        Args:
            config: Bot configuration
            bot: Optional bot instance (will be created if not provided)
        """
        self.config = config
        self.bot = bot or config.bot
        
        # Default startup image (can be overridden from config)
        self.startup_image: str = config.STARTUP_IMAGE or "https://files.catbox.moe/ehv507.jpeg"
        
        # Owner display name
        self.owner_name: str = config.OWNER_DISPLAY_NAME or f"@{config.OWNER_ID}"
    
    async def send_startup_message(self) -> Optional[Message]:
        """
        Send a startup notification to the logging channel.
        
        Returns:
            The sent message if successful, None otherwise
        """
        try:
            if not self.config.BOT_LOGGING:
                logger.warning("No logging channel configured for startup message")
                return None
            
            caption = self._format_startup_caption()
            
            # Use send_photo with caption
            message = await self.bot.send_photo(
                chat_id=self.config.get_logging_target(),
                photo=self.startup_image,
                caption=caption,
                parse_mode="HTML",
            )
            
            logger.info("✅ Startup notification sent successfully")
            return message
            
        except Exception as e:
            logger.error(f"❌ Failed to send startup notification: {e}")
            return None
    
    async def send_status_update(
        self,
        status: str,
        emoji: str = "ℹ️",
        details: Optional[dict] = None
    ) -> Optional[Message]:
        """
        Send a status update to the logging channel.
        
        Args:
            status: Status message
            emoji: Emoji prefix
            details: Additional details to include
            
        Returns:
            The sent message if successful, None otherwise
        """
        try:
            if not self.config.BOT_LOGGING:
                return None
            
            text = f"{emoji} <b>Status Update</b>\n\n{status}"
            
            if details:
                text += "\n\n<b>Details:</b>\n"
                for key, value in details.items():
                    text += f"• <code>{key}</code>: {value}\n"
            
            message = await self.bot.send_message(
                chat_id=self.config.get_logging_target(),
                text=text,
                parse_mode="HTML",
            )
            
            return message
            
        except Exception as e:
            logger.error(f"❌ Failed to send status update: {e}")
            return None
    
    async def send_error_alert(
        self,
        error: Exception,
        context: Optional[str] = None
    ) -> Optional[Message]:
        """
        Send an error alert to the logging channel.
        
        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
            
        Returns:
            The sent message if successful, None otherwise
        """
        try:
            if not self.config.BOT_LOGGING:
                return None
            
            text = f"⚠️ <b>Error Alert</b>\n\n"
            
            if context:
                text += f"<b>Context:</b> {context}\n\n"
            
            text += f"<b>Error:</b> {type(error).__name__}\n"
            text += f"<b>Message:</b> <code>{str(error)}</code>"
            
            message = await self.bot.send_message(
                chat_id=self.config.get_logging_target(),
                text=text,
                parse_mode="HTML",
            )
            
            return message
            
        except Exception as e:
            logger.error(f"❌ Failed to send error alert: {e}")
            return None
    
    async def send_to_owner(self, text: str, parse_mode: str = "HTML") -> Optional[Message]:
        """
        Send a private message to the bot owner.
        
        Args:
            text: Message text
            parse_mode: Parse mode for the message
            
        Returns:
            The sent message if successful, None otherwise
        """
        try:
            message = await self.bot.send_message(
                chat_id=self.config.OWNER_ID,
                text=text,
                parse_mode=parse_mode,
            )
            return message
        except Exception as e:
            logger.error(f"❌ Failed to send message to owner: {e}")
            return None
    
    async def send_to_channel(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: str = "HTML",
        photo: Optional[str] = None
    ) -> Optional[Message]:
        """
        Send a message to a specific channel or chat.
        
        Args:
            chat_id: Target chat ID or username
            text: Message text
            parse_mode: Parse mode
            photo: Optional photo URL to send
            
        Returns:
            The sent message if successful, None otherwise
        """
        try:
            if photo:
                message = await self.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=text,
                    parse_mode=parse_mode,
                )
            else:
                message = await self.bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode=parse_mode,
                )
            return message
        except Exception as e:
            logger.error(f"❌ Failed to send message to channel {chat_id}: {e}")
            return None
    
    def _format_startup_caption(self) -> str:
        """
        Format the startup message caption.
        
        Returns:
            HTML-formatted caption string
        """
        import datetime
        
        # Get current time
        current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        # Build caption
        caption = (
            "🤖 <b>WaifuBot is Online!</b>\n\n"
            f"🧑‍💻 <b>Owner:</b> {self.owner_name}\n"
            f"🕐 <b>Time:</b> {current_time}\n"
            f"📊 <b>Status:</b> 🟢 All systems operational\n\n"
            f"🦋 <b>Bot Version:</b> 2.0.0\n"
            f"💎 <b>Framework:</b> Aiogram 3.x"
        )
        
        # Add force join link if available
        if self.config.FORCE_JOIN_LINK:
            caption += f"\n\n🔗 <b>Force Join:</b> {self.config.FORCE_JOIN_LINK}"
        
        return caption


# Legacy compatibility function
async def send_start_message_legacy(config: Config, bot: Bot) -> None:
    """
    Legacy function for sending start message.
    Maintained for backward compatibility.
    
    Args:
        config: Bot configuration
        bot: Bot instance
    """
    service = NotificationService(config, bot)
    await service.send_startup_message()


# Convenience function to create a notification service
def create_notification_service(config: Config, bot: Optional[Bot] = None) -> NotificationService:
    """
    Create a notification service instance.
    
    Args:
        config: Bot configuration
        bot: Optional bot instance
        
    Returns:
        NotificationService instance
    """
    return NotificationService(config, bot)
