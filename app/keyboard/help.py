# ==========================================
# Help Keyboard
# ==========================================

"""
Inline keyboards for help system.
"""

from typing import Dict, List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_help_keyboard(help_data: Dict[str, Dict]) -> InlineKeyboardMarkup:
    """
    Get the keyboard for help menu.
    
    Args:
        help_data: Help data dictionary
        
    Returns:
        InlineKeyboardMarkup
    """
    buttons = []
    
    # Sort by display name
    sorted_modules = sorted(
        help_data.items(),
        key=lambda x: x[1].get("HELP_NAME", x[0])
    )
    
    for module_name, module_data in sorted_modules:
        button_name = module_data.get("HELP_NAME", module_name.capitalize())
        buttons.append(
            InlineKeyboardButton(
                f"📋 {button_name}",
                callback_data=f"help_{module_name}",
            )
        )
    
    # Split into 2 columns
    keyboard_rows = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    
    # Add back button
    keyboard_rows.append([
        InlineKeyboardButton(
            "⬅️ Return to main menu",
            callback_data="back_to_home",
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)


def get_module_keyboard() -> InlineKeyboardMarkup:
    """
    Get the keyboard for module help.
    
    Returns:
        InlineKeyboardMarkup
    """
    buttons = [
        [
            InlineKeyboardButton(
                "⬅️ Back to categories",
                callback_data="open_help",
            )
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
