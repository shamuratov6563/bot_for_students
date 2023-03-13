from aiogram.dispatcher.filters import Filter
from aiogram import types

ADMIN = 385419373

admins = [ADMIN, ]


class IsAdmin(Filter):
    key = 'is_admin'

    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in admins