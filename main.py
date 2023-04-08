from aiogram import Bot, Dispatcher, executor, types
from keyboards import get_keyboards, get_all_section_ikb, \
    get_admin_kb, get_lessons_by_sec, get_actions_lesson_kb, get_approval, get_sections_for_admin, \
    get_actions_sections_kb, get_approval_lesson_ikb, get_sections_for_new_lesson_ikb, get_edit_lesson_ikb, \
    get_sections_ikb
from aiogram.dispatcher.filters import Text
from sqlite import db_start, get_lesson, create_section, get_section, get_all_sections_name, \
    delete_section, get_lesson_name, get_all_lessons_name, create_lesson, delete_lesson, \
    edit_lesson_video_sql, edit_lession_name_sql, \
    edit_lesson_handout_sql, edit_lesson_homework_sql, edit_lesson_section_id_sql
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from filter import IsAdmin, admins

try:
    from local_settings import TOKEN
except Exception as e:
    print(e)
PROXY_URL = "http://proxy.server:3128"

bot = Bot(token=TOKEN, proxy=PROXY_URL)

dp = Dispatcher(bot, storage=MemoryStorage())

# id for recognizing lesson
lesson_id = None


class SectionStatesGroup(StatesGroup):
    name = State()


class LessonStatesGroup(StatesGroup):
    name = State()
    video = State()
    handout = State()
    homework = State()
    section_id = State()


class LessonEditStatesGroup(StatesGroup):
    name = State()
    video = State()
    handout = State()
    homework = State()
    section_id = State()


async def on_startup(_):
    await db_start()
    print("Db successfully started")


# @dp.message_handler(commands=['Cancel'], state='*')
# async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await message.reply('Canceled')


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Soff Study Backend kursi o'quvchilari uchun "
                         "yaratilgan botga hush kelibsiz!",
                         reply_markup=get_keyboards())
    await message.delete()


@dp.message_handler(Text(equals='Darslar ro\'yhati'))
async def process_lessons_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Yo\'nalishni tanlang', reply_markup=get_all_section_ikb())
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
    if callback_query.from_user.id in admins:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"<b>{text}</b>",
                               parse_mode=types.ParseMode.HTML,
                               reply_markup=get_actions_lesson_kb(callback_query.data[2:]))
    else:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"<b>{text}</b>",
                               parse_mode=types.ParseMode.HTML)

    await callback_query.message.delete()


# ADMIN PANEL
@dp.message_handler(Text(equals='Yangi bo\'lim qo\'shish'), IsAdmin())
async def adding_new_section(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Yangi Bo'lim uchun nom kiriting:")

    await SectionStatesGroup.name.set()


# Adding New Section
@dp.message_handler(IsAdmin(), state=SectionStatesGroup.name)
async def adding_new_section_name(message: types.Message, state: FSMContext):
    sections = get_all_sections_name()
    secs = []
    for sec in sections:
        secs.append(sec[0])
    if message.text not in secs:
        async with state.proxy() as data:
            data['name'] = message.text
        await create_section(message.text)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Yangi Bo'lim qo'shildi",
                               reply_markup=get_admin_kb())
        await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Bunday nomli bo'lim allaqachon mavjud boshqa nom kiriting")

    await message.delete()


# Modify Section
@dp.message_handler(Text(equals='Bo\'limlar ro\'yhati'), IsAdmin())
async def modify_section(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Bo'limlar ro'yhati:",
                           reply_markup=get_sections_for_admin())

    await message.delete()


@dp.callback_query_handler(lambda c: c.data.startswith('a_s_'), IsAdmin())
async def process_modify_section_callback(callback_query: types.CallbackQuery):
    section_name = get_section(callback_query.data[4:])
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"{section_name} bo'limi ustida amallar bajarish",
                           reply_markup=get_actions_sections_kb(section_id=callback_query.data[4:]))

    await callback_query.message.delete()


# Delete Section
@dp.callback_query_handler(lambda c: c.data.startswith('admin_sd_'), IsAdmin())
async def process_delete_section_callback(callback_query: types.CallbackQuery):
    section_name = get_section(callback_query.data[9:])
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"{section_name} bo'limini o'chirishni tasdiqlaysizmi?",
                           reply_markup=get_approval(section_id=callback_query.data[9:]))

    await callback_query.message.delete()


# Approve to delete section
@dp.callback_query_handler(lambda c: c.data.startswith('ad_'), IsAdmin())
async def process_delete_section_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await delete_section(callback_query.data[3:])
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"Bo'lim o'chirildi",
                           reply_markup=get_admin_kb())

    await callback_query.message.delete()


# Modify section name
# TO DO : Modify section name

# Adding New Lesson
@dp.message_handler(Text(equals='Yangi dars qo\'shish'), IsAdmin())
async def adding_new_lesson(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Yangi darsni qo'shmoqchi bo'lgan bo'limni tanlang:",
                           reply_markup=get_sections_for_new_lesson_ikb())

    await LessonStatesGroup.section_id.set()


@dp.callback_query_handler(lambda c: c.data.startswith('nl_s_'), IsAdmin(), state=LessonStatesGroup.section_id)
async def process_adding_new_lesson_section_callback(callback_query: types.CallbackQuery, state: FSMContext):
    section_name = get_section(callback_query.data[5:])
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        data['section_id'] = callback_query.data[5:]
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"Yangi dars nom kiriting?")

    await LessonStatesGroup.name.set()


@dp.message_handler(IsAdmin(), state=LessonStatesGroup.name)
async def adding_new_lesson_name(message: types.Message, state: FSMContext):
    lesson_name = get_all_lessons_name()
    lessons = []
    if lesson_name is not None:
        for lesson in lesson_name:
            lessons.append(lesson[0])
    if message.text not in lessons:
        async with state.proxy() as data:
            data['name'] = message.text

        await bot.send_message(chat_id=message.from_user.id,
                               text="Yangi dars uchun video linkini jo'nating:")
        await LessonStatesGroup.video.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Bunday nomli dars allaqachon mavjud boshqa nom kiriting: ")

        await message.delete()


@dp.message_handler(IsAdmin(), state=LessonStatesGroup.video)
async def adding_new_lesson_video(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['video'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Yangi dars uchun slidning linkini jo'nating:")
    await LessonStatesGroup.handout.set()


@dp.message_handler(IsAdmin(), state=LessonStatesGroup.handout)
async def adding_new_lesson_handout(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['handout'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Yangi dars uchun darslikning uyga vazifasini linkini jo'nating:")
    await LessonStatesGroup.homework.set()


# Last step to add new lesson
@dp.message_handler(IsAdmin(), state=LessonStatesGroup.homework)
async def adding_new_lesson_homework(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['homework'] = message.text
    await create_lesson(data['name'], data['video'], data['handout'], data['homework'], data['section_id'])
    await bot.send_message(chat_id=message.from_user.id,
                           text="Darslik muvaffaqiyatli qo'shildi")
    await state.finish()


# Delete Lesson
@dp.callback_query_handler(lambda c: c.data.startswith('d_'), IsAdmin())
async def process_delete_lesson_callback(callback_query: types.CallbackQuery):
    lesson_name = await get_lesson_name(callback_query.data[2:])
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"{lesson_name} darsini o'chirishni tasdiqlaysizmi?",
                           reply_markup=get_approval_lesson_ikb(lesson_id=callback_query.data[2:]))

    await callback_query.message.delete()


# Lesson deleted
@dp.callback_query_handler(lambda c: c.data.startswith('adl_'), IsAdmin())
async def process_delete_lesson_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await delete_lesson(callback_query.data[4:])
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"Dars o'chirildi",
                           reply_markup=get_admin_kb())

    await callback_query.message.delete()


# Modify Lesson Name
@dp.callback_query_handler(lambda c: c.data.startswith('e_'), IsAdmin())
async def process_edit_lesson_callback(callback_query: types.CallbackQuery):
    lesson_name = await get_lesson_name(callback_query.data[2:])
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"{lesson_name} darsining o'zgartirmoqchi bo'lgan qismini tanlang:",
                           reply_markup=get_edit_lesson_ikb(callback_query.data[2:]))


@dp.callback_query_handler(lambda c: c.data.startswith('lesson_edit_'), IsAdmin())
async def process_edit_lesson_callback(callback_query: types.CallbackQuery):
    global lesson_id
    lesson_id = callback_query.data[11:]
    if 'name' in callback_query.data:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"Dars nomini kiriting:")
        await LessonEditStatesGroup.name.set()
    elif 'video' in callback_query.data:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"Dars uchun video linkini kiriting:")
        await LessonEditStatesGroup.video.set()
    elif 'slide' in callback_query.data:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"Dars uchun slidning linkini kiriting:")
        await LessonEditStatesGroup.handout.set()
    elif 'homework' in callback_query.data:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"Dars uchun darslikning uyga vazifasini linkini kiriting:")
        await LessonEditStatesGroup.homework.set()
    await callback_query.message.delete()


@dp.message_handler(IsAdmin(), state=LessonEditStatesGroup.name)
async def edit_lesson_name(message: types.Message, state: FSMContext):
    global lesson_id
    lesson_id = lesson_id[6:]
    async with state.proxy() as data:
        data['name'] = message.text
    await edit_lession_name_sql(data['name'], lesson_id)
    await bot.send_message(chat_id=message.from_user.id,
                           text="Dars nomi muvaffaqiyatli o'zgartirildi")
    await state.finish()


@dp.message_handler(IsAdmin(), state=LessonEditStatesGroup.video)
async def edit_lesson_video(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['video'] = message.text
    await edit_lesson_video_sql(data['video'], lesson_id[7:])
    await bot.send_message(chat_id=message.from_user.id,
                           text="Dars uchun video linki muvaffaqiyatli o'zgartirildi")
    await state.finish()


@dp.message_handler(IsAdmin(), state=LessonEditStatesGroup.handout)
async def edit_lesson_handout(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['handout'] = message.text
    await edit_lesson_handout_sql(data['handout'], lesson_id[7:])
    await bot.send_message(chat_id=message.from_user.id,
                           text="Dars uchun slidning linki muvaffaqiyatli o'zgartirildi")
    await state.finish()


@dp.message_handler(IsAdmin(), state=LessonEditStatesGroup.homework)
async def edit_lesson_homework(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['homework'] = message.text
    await edit_lesson_homework_sql(data['homework'], lesson_id[10:])
    await bot.send_message(chat_id=message.from_user.id,
                           text="Dars uchun darslikning uyga vazifasining linki muvaffaqiyatli o'zgartirildi")
    await state.finish()


if __name__ == '__main__':
    dp.bind_filter(IsAdmin)
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
