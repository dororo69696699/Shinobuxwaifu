from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from config import OWNER_ID


class OwnerFilter(Filter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return event.from_user.id == OWNER_ID
