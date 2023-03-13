from aiogram import Bot, Dispatcher, executor, types
from keyboards import get_keyboards, get_all_section, \
    get_admin_kb, get_lessons_by_sec, get_actions_kb, get_approval, get_sections_for_admin
from aiogram.dispatcher.filters import Text
from sqlite import db_start, get_lesson, create_section, get_section
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

try:
    from local_settings import TOKEN
except Exception as e:
    print(e)

from filter import IsAdmin

bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())


class SectionStatesGroup(StatesGroup):
    name = State()


class LessonStateGroup(StatesGroup):
    name = State()
    video = State()
    handout = State()
    homework = State()
    section_id = State()


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
    await message.delete()


@dp.message_handler(Text(equals='Admin paneli'), IsAdmin())
async def process_admin_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Admin paneliga xush kelibsiz, {message.from_user.full_name}",
                           reply_markup=get_admin_kb())

    await message.delete()


@dp.callback_query_handler(lambda c: c.data.startswith('s_'))
async def process_section_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="<b>Tanlangan yo'nalish bo'yicha darslar ro'yxati</b>",
                           reply_markup=get_lessons_by_sec(callback_query.data[2:]),
                           parse_mode=types.ParseMode.HTML)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data.startswith('l_'))
async def process_lesson_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    lesson = get_lesson(callback_query.data[2:])
    text = f"""
        Dars nomi : <b>{lesson[1]}</b>,
        Dars video linki : {lesson[2]},
        Dars Fayli : {lesson[3]},
        Uyga vazifa : {lesson[4]}
    """
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"<b>{text}</b>",
                           parse_mode=types.ParseMode.HTML,
                           reply_markup=get_actions_kb(callback_query.data[2:]))


# ADMIN PANEL
@dp.message_handler(Text(equals='Yangi bo\'lim qo\'shish'), IsAdmin())
async def adding_new_section(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Yangi Bo'lim uchun nom kiriting:")

    await SectionStatesGroup.name.set()


# Adding New Section
@dp.message_handler(IsAdmin(), state=SectionStatesGroup.name)
async def adding_new_section_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await create_section(message.text)
    await message.answer("Yangi Bo'lim uchun video linki kiriting:")
    await SectionStatesGroup.next()


# Modify Section
@dp.message_handler(Text(equals='Bo\'limlar ro\'yhati'), IsAdmin())
async def modify_section(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Bo'limlar ro'yhati:",
                           reply_markup=get_sections_for_admin())


@dp.callback_query_handler(lambda c: c.data.startswith('a_s_'), IsAdmin())
async def process_delete_section_callback(callback_query: types.CallbackQuery):
    section_name = get_section(callback_query.data[2:])
    print(section_name)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"{section_name} bo'limini o'chirishni tasdiqlaysizmi?",
                           reply_markup=get_approval(section_id=callback_query.data[2:]))


if __name__ == '__main__':
    dp.bind_filter(IsAdmin)
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
