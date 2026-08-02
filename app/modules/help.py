
# ==========================================
# Help Command Handler
# ==========================================

"""
Help Command Handler

Provides help system with categorized modules and navigation.
"""

import logging
from typing import Dict, List, Optional

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.assets.help import get_help_data
from app.keyboards.help import get_help_keyboard, get_module_keyboard
from app.core.config import Config

logger = logging.getLogger(__name__)

router = Router(name="help")


@router.message(Command("help"))
async def help_command(
    message: Message,
    config: Config,
) -> None:
    """
    Handle /help command.
    
    Args:
        message: Incoming message
        config: Bot configuration
    """
    help_data = get_help_data(config.BOT_USERNAME or "")
    keyboard = get_help_keyboard(help_data)
    
    text = (
        "⚙️ <b>Help Menu</b>\n\n"
        "<blockquote>\n"
        "Select a category to explore available commands and guides.\n\n"
        "All commands use the prefix: <code>/</code>\n"
        "</blockquote>"
    )
    
    await message.reply(
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@router.callback_query(lambda c: c.data == "open_help")
async def help_callback(
    callback: CallbackQuery,
    config: Config,
) -> None:
    """
    Handle help button callback.
    
    Args:
        callback: Callback query
        config: Bot configuration
    """
    help_data = get_help_data(config.BOT_USERNAME or "")
    keyboard = get_help_keyboard(help_data)
    
    text = (
        "⚙️ <b>Help Menu</b>\n\n"
        "<blockquote>\n"
        "Select a category to explore available commands and guides.\n\n"
        "All commands use the prefix: <code>/</code>\n"
        "</blockquote>"
    )
    
    await callback.answer()
    
    try:
        await callback.message.edit_caption(
            caption=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    except Exception:
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )


@router.callback_query(lambda c: c.data.startswith("help_"))
async def help_module_callback(
    callback: CallbackQuery,
    config: Config,
) -> None:
    """
    Handle help module callback.
    
    Args:
        callback: Callback query
        config: Bot configuration
    """
    module_name = callback.data.split("_", 1)[1]
    help_data = get_help_data(config.BOT_USERNAME or "")
    
    module_data = help_data.get(module_name, {})
    help_text = module_data.get("HELP", "Module help not available.")
    help_name = module_data.get("HELP_NAME", module_name.capitalize())
    
    text = (
        f"📚 <b>{help_name}</b>\n\n"
        f"<blockquote>\n{help_text}\n</blockquote>"
    )
    
    keyboard = get_module_keyboard()
    
    await callback.answer()
    
    try:
        await callback.message.edit_caption(
            caption=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    except Exception:
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )


@router.callback_query(lambda c: c.data == "back_to_home")
async def back_home_callback(
    callback: CallbackQuery,
    config: Config,
) -> None:
    """
    Handle back to home callback.
    
    Args:
        callback: Callback query
        config: Bot configuration
    """
    help_data = get_help_data(config.BOT_USERNAME or "")
    keyboard = get_help_keyboard(help_data)
    
    text = (
        "⚙️ <b>Help Menu</b>\n\n"
        "<blockquote>\n"
        "Select a category to explore available commands and guides.\n\n"
        "All commands use the prefix: <code>/</code>\n"
        "</blockquote>"
    )
    
    await callback.answer()
    
    try:
        await callback.message.edit_caption(
            caption=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    except Exception:
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
