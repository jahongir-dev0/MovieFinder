from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from data.config import ADMINS  # ADMINS bu yerda ro'yxat bo'lishi kerak

class AdminFilter(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.from_user.id in ADMINS  # Admin ID ro'yxatda borligini tekshirish