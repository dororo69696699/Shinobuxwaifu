
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_help_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("💰 Balance", callback_data="help_balance"),
            InlineKeyboardButton("🎯 Guess", callback_data="help_guess"),
        ],
        [
            InlineKeyboardButton("🛒 Shop", callback_data="help_shop"),
            InlineKeyboardButton("🌸 Harem", callback_data="help_harem"),
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="back_to_home"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
