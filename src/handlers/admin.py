import enum

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery

from src.database import ORM

router = Router()


class AdminCommands(enum.Enum):
    SHOW_COUNT = "show_count"


class AdminCallbackData(CallbackData):
    action: str


def admin_commands_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text='Users count', callback_data=AdminCallbackData(action=command.value).pack())
        ] for command in AdminCommands
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("admin"))
async def cmd_admin_menu(message: Message):
    await message.answer('Commands:', reply_markup=admin_commands_kb())


@router.callback_query(AdminCallbackData.filter())
async def show_users_count(callback: CallbackQuery, callback_data: AdminCallbackData):

    if callback_data.action == AdminCommands.SHOW_COUNT.value:
        count = await ORM.select_user_count()
        await callback.message.answer(f"Count: {count}")


