from aiogram import Router
from modules.sudo import toggle_power, close_keyboard

router = Router(name="sudo_callbacks")

router.callback_query(toggle_power)
router.callback_query(close_keyboard)
