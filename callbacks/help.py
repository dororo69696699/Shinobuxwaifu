from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.help import get_help_keyboard

router = Router(name="help_callbacks")


@router.callback_query(lambda c: c.data == "open_help")
async def open_help(callback: CallbackQuery) -> None:
    await callback.answer()
    
    text = "⚙️ <b>Help Menu</b>\n\nSelect a category to explore commands."
    
    await callback.message.edit_text(
        text=text,
        reply_markup=get_help_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(lambda c: c.data == "back_to_home")
async def back_to_home(callback: CallbackQuery) -> None:
    await callback.answer()
    
    from modules.start import start_command
    await start_command(callback.message)
