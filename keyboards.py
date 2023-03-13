from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import sqlite as db
from sqlite import get_all_lessons_by_sec, get_all_sections, get_lesson


def get_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Asosiy menyu', callback_data='b_1')],
    ])

    return ikb


def get_admin_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Bo\'limlar ro\'yhati"), KeyboardButton("Darslar ro\'yhati"))
    kb.add(KeyboardButton('Yangi dars qo\'shish'), KeyboardButton('Yangi bo\'lim qo\'shish'))
    return kb


def get_keyboards() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Darslar ro\'yxati'))
    kb.add(KeyboardButton('Intervyu savollari'))
    kb.add(KeyboardButton('Admin paneli'))

    return kb


def get_all_section() -> InlineKeyboardMarkup:
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


def get_lessons_by_sec(sec) -> InlineKeyboardMarkup:
    lessons = get_all_lessons_by_sec(sec)
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lesson[1], callback_data=f'l_{lesson[0]}')]
        for lesson in lessons
    ])
    return ikb


def get_actions_kb(section_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Darsni tahrirlash', callback_data=f'e_{section_id}')],
        [InlineKeyboardButton(text='Darsni o\'chirish', callback_data=f'd_{section_id}')],
        [InlineKeyboardButton(text='Asosiy menyu', callback_data='b_1')],
    ])

    return ikb


def get_approval(section_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ha", callback_data=f"ad_{section_id}")],
        [InlineKeyboardButton(text="Yo'q", callback_data=f"bd_{section_id}")],
    ])

    return ikb
