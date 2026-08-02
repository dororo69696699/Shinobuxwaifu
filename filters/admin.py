
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from config import OWNER_ID
from database.models import is_vip


class AdminFilter(Filter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return event.from_user.id == OWNER_ID


class AdminOrVIPFilter(Filter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = event.from_user
        if user.id == OWNER_ID:
            return True
        return await is_vip(user.id)
