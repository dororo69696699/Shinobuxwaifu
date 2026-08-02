# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

"""
Logging Utilities
"""

import logging
from config import BOT_LOGGING


async def send_log_message(app, chat_id: int, message: str):
    """Send a log message to the specified chat."""
    try:
        await app.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logging.error(f"Failed to send log message: {e}")
