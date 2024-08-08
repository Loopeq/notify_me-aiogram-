from typing import List

from aiogram import types
from aiogram.filters.callback_data import CallbackData

from src.models import NotificationGetDTO
from src.strings import Languages, strings


class LanguageCallbackData(CallbackData, prefix="lang"):
    value: str


def select_language_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text="ru🇷🇺",
                                       callback_data=LanguageCallbackData(value=Languages.RU.value).pack()),
            types.InlineKeyboardButton(text="en🇬🇧",
                                       callback_data=LanguageCallbackData(value=Languages.EN.value).pack())
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def main_menu_kb(lang: str, is_current_exist: bool = True):
    phrases = strings[lang]['main']
    buttons = [
        [
            types.KeyboardButton(text=phrases['add']),
            types.KeyboardButton(text=phrases['all']),
        ],
        [
            types.KeyboardButton(text=phrases['stop_current'] if is_current_exist else phrases['no_current'])
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons,
                                         resize_keyboard=True,
                                         is_persistent=True)
    return keyboard


def notification_interval_kb():
    buttons = [
        [types.KeyboardButton(text=f'{j}m') for j in range(5, 25, 5)],
        [types.KeyboardButton(text=f'{j}m') for j in range(25, 65, 5)],
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True,
                                         is_persistent=False)
    return keyboard


class NotificationCallbackData(CallbackData, prefix="not"):
    not_id: int


def notification_list_kb(notifications: List[NotificationGetDTO]):
    buttons = [
        [types.InlineKeyboardButton(text=f"[Every {notification.minutes}m] - {notification.title}",
                                    callback_data=NotificationCallbackData(not_id=notification.id).pack())]
        for notification in notifications
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

