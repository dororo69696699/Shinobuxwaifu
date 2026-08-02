
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_back_button(callback_data: str = "back_to_home") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("⬅️ Back", callback_data=callback_data)]
    ])


def get_yes_no_buttons(yes_data: str = "confirm", no_data: str = "cancel") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton("✅ Yes", callback_data=yes_data),
            InlineKeyboardButton("❎ No", callback_data=no_data),
        ]
    ])
