from aiogram.dispatcher.filters import Filter
from aiogram import types
try:
    from local_settings import ADMIN
except Exception as e:
    print(e)
admins = [ADMIN, ]


class IsAdmin(Filter):
    key = 'is_admin'

    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in admins