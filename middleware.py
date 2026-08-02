# ==========================================
# Middleware Setup
# ==========================================

import logging
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """Log all messages."""
    
    async def __call__(self, handler, event: Message, data: dict):
        if isinstance(event, Message):
            logger.debug(f"Message from {event.from_user.id}: {event.text}")
        return await handler(event, data)


async def setup_middleware(dp: Dispatcher):
    """Setup all middleware."""
    dp.message.middleware(LoggingMiddleware())
