from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import sqlite as db
from sqlite import get_all_lessons_by_sec, get_all_sections, get_lesson


# def get_cancel_ikb() -> ReplyKeyboardMarkup:
#     return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/Cancel'))


def get_admin_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Bo\'limlar ro\'yhati"), KeyboardButton("Darslar ro\'yhati"))
    kb.add(KeyboardButton('Yangi bo\'lim qo\'shish'), KeyboardButton('Yangi dars qo\'shish'))
    return kb


def get_keyboards() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Darslar ro\'yhati'))
    kb.add(KeyboardButton('Admin paneli'))

    return kb


def get_all_section_ikb() -> InlineKeyboardMarkup:
    sections = get_all_sections()
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=section[1], callback_data=f's_{section[0]}')]
        for section in sections
    ])
    return ikb


def get_sections_for_admin() -> InlineKeyboardMarkup:
    sections = get_all_sections()
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=section[1], callback_data=f'a_s_{section[0]}')]
        for section in sections
    ])
    return ikb


def get_sections_for_new_lesson_ikb() -> InlineKeyboardMarkup:
    sections = get_all_sections()
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=section[1], callback_data=f'nl_s_{section[0]}')]
        for section in sections
    ])
    return ikb


def get_lessons_by_sec(sec) -> InlineKeyboardMarkup:
    lessons = get_all_lessons_by_sec(sec)
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lesson[1], callback_data=f'l_{lesson[0]}')]
        for lesson in lessons
    ])
    return ikb


def get_actions_sections_kb(section_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Bo'limni tahrirlash", callback_data=f"admin_se_{section_id}")],
        [InlineKeyboardButton(text="Bo'limni o'chirish", callback_data=f"admin_sd_{section_id}")],
    ])

    return ikb


# actions for lessons
def get_actions_lesson_kb(lesson_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Darsni tahrirlash', callback_data=f'e_{lesson_id}')],
        [InlineKeyboardButton(text='Darsni o\'chirish', callback_data=f'd_{lesson_id}')],
    ])

    return ikb


def get_approval(section_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ha", callback_data=f"ad_{section_id}")],
        [InlineKeyboardButton(text="Yo'q", callback_data=f"a_s_{section_id}")],
    ])

    return ikb


def get_approval_lesson_ikb(lesson_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ha", callback_data=f"adl_{lesson_id}")],
        [InlineKeyboardButton(text="Yo'q", callback_data=f"l_{lesson_id}")],
    ])

    return ikb


def get_edit_lesson_ikb(lesson_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Dars nomi", callback_data=f"lesson_edit_name_{lesson_id}")],
        [InlineKeyboardButton(text="Dars videosi", callback_data=f"lesson_edit_video_{lesson_id}")],
        [InlineKeyboardButton(text="Dars slaydi", callback_data=f"lesson_edit_slide_{lesson_id}")],
        [InlineKeyboardButton(text="Dars vazifasi", callback_data=f"lesson_edit_homework_{lesson_id}")],
    ])

    return ikb


def get_sections_ikb() -> InlineKeyboardMarkup:
    sections = get_all_sections()
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=section[1], callback_data=f'admin_s_{section[0]}')]
        for section in sections
    ])
    return ikb
