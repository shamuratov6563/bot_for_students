from aiogram import Bot, Dispatcher, executor, types
from keyboards import get_keyboards, get_all_section, get_admin_kb
from aiogram.dispatcher.filters import Text
from sqlite import db_start

try:
    from local_settings import TOKEN
except Exception as e:
    print(e)

from filter import IsAdmin


bot = Bot(token=TOKEN)

dp = Dispatcher(bot)


async def on_startup(_):
    await db_start()
    print("Db successfully started")


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Soff Study Backend kursi o'quvchilari uchun "
                         "yaratilgan botga hush kelibsiz!",
                         reply_markup=get_keyboards())
    await message.delete()


@dp.message_handler(Text(equals='Darslar ro\'yxati'))
async def process_lessons_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                            text='Yo\'nalishni tanlang', reply_markup=get_all_section())


@dp.message_handler(Text(equals='Admin paneli'), IsAdmin())
async def process_admin_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Admin paneliga xush kelibsiz, {message.from_user.full_name}",
                           reply_markup=get_admin_kb())



if __name__ == '__main__':
    dp.bind_filter(IsAdmin)
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
