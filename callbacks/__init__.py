
from aiogram import Dispatcher
from callbacks.help import router as help_router


def register_all_callbacks(dp: Dispatcher):
    dp.include_router(help_router)
