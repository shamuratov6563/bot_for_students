from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import sqlite as db
from sqlite import get_all_lessons, get_all_sections


def get_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Asosiy menyu', callback_data='b_1')],
    ])

    return ikb


def get_admin_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Yangi dars qo\'shish'), KeyboardButton('Yangi bo\'lim qo\'shish'))
    kb.add(KeyboardButton('Darsni tahrirlash'), KeyboardButton('Bo\'limni tahrirlash'))
    kb.add(KeyboardButton('Darsni o\'chirish'), KeyboardButton('Bo\'limni o\'chirish'))
    return kb


def get_keyboards() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Darslar ro\'yxati'))
    kb.add(KeyboardButton('Foydali manbalar'))
    kb.add(KeyboardButton('Intervyu savollari'))
    kb.add(KeyboardButton('Admin paneli'))

    return kb


def get_all_section() -> InlineKeyboardMarkup:
    sections = get_all_sections()
    for section in sections:
        print(section)
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=section[0], callback_data=f's_{section[0]}')]
        for section in sections
    ])
    return ikb
