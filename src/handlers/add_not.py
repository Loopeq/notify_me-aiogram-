import datetime

from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from src.database import ORM
from src.keyboards import notification_interval_kb, cancel_create_notification_button
from src.models import NotificationDTO
from src.strings import strings
from ..bot_config import BotCommands
router = Router()


class AddNotification(StatesGroup):
    minutes = State()
    title = State()


@router.message(F.text.in_({'Cancel❌', "Отменить❌"}))
async def cancel_add_notification(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="❌Отменено", reply_markup=ReplyKeyboardRemove())


@router.message(Command(BotCommands.ADD_NOT.value))
async def add_notification(message: Message, state: FSMContext):
    lang = await ORM.select_user_language(user_id=message.from_user.id)
    await message.answer(strings[lang]['add_not'], reply_markup=notification_interval_kb(lang=lang))
    await state.set_state(AddNotification.minutes)


@router.message(F.text, AddNotification.minutes)
async def get_notification_minutes(message: Message, state: FSMContext):
    lang = await ORM.select_user_language(user_id=message.from_user.id)
    minutes = message.text.replace("m", "")
    if not minutes.isdigit():
        await message.answer(strings[lang]['add_not_expt'])
        return

    if not int(minutes) in range(1, 500):
        await message.answer(strings[lang]['add_not_interval'])
        return
    else:
        await message.answer(strings[lang]["add_not_ph"],
                             reply_markup=cancel_create_notification_button(lang=lang))
        await state.update_data(minutes=minutes)
        await state.set_state(AddNotification.title)


@router.message(F.text, AddNotification.title)
async def get_notification_title(message: Message, state: FSMContext):

    title_length = 50
    lang = await ORM.select_user_language(user_id=message.from_user.id)

    if len(message.text) > title_length:
        await message.answer(strings[lang]['add_not_len_expt'])
        return

    data = await state.get_data()
    title = message.text
    minutes = data['minutes']
    notification = NotificationDTO(user_id=message.from_user.id,
                                   minutes=int(minutes),
                                   title=title,
                                   created_at=datetime.datetime.utcnow())
    await ORM.insert_notification(notification=notification)
    await state.clear()
    await message.answer(strings[lang]['not_ready'].format(notification.title, notification.minutes),
                         reply_markup=ReplyKeyboardRemove())


