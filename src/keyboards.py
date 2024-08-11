import enum
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


def notification_interval_kb(lang: str):
    buttons = [
        [types.KeyboardButton(text=f'{j}m') for j in range(5, 35, 5)],
        [types.KeyboardButton(text=f"{strings[lang]['cancel']}")]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True,
                                         input_field_placeholder=strings[lang]['min_placeholder'],
                                         is_persistent=True)
    return keyboard


class NotificationCBActions(enum.Enum):
    SHOW = "show"
    DELETE = 'delete'


class NotificationCallbackData(CallbackData, prefix="not"):
    action: NotificationCBActions
    not_id: int


def notification_list_kb(notifications: List[NotificationGetDTO]):
    buttons = [
        [types.InlineKeyboardButton(text=f"[Every {notification.minutes}m] - {notification.title}",
                                    callback_data=NotificationCallbackData(not_id=notification.id,
                                                                           action=NotificationCBActions.SHOW).pack()),
         types.InlineKeyboardButton(text="❌", callback_data=NotificationCallbackData(not_id=notification.id,
                                                                                     action=NotificationCBActions.DELETE).pack())]
        for notification in notifications
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def cancel_create_notification_button(lang: str):
    button = [
        [types.KeyboardButton(text=f"{strings[lang]['cancel']}")]
    ]

    return types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True,
                                     is_persistent=True)


class ProcessKillerCallbackData(CallbackData, prefix='stop_not'):
    message_id: int
    not_id: int


def kill_running_notification_button(message_id: int, not_id: int):
    button = [
        [types.InlineKeyboardButton(text=strings['common']['stop_notification'],
                                    callback_data=ProcessKillerCallbackData(message_id=message_id,
                                                                            not_id=not_id).pack())]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=button)


