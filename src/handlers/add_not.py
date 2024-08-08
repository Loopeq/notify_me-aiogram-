import datetime

from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from src.database import ORM
from src.keyboards import notification_interval_kb, main_menu_kb
from src.models import NotificationDTO, RunningSessionDTO
from src.sheduler import run_scheduler
from src.strings import strings

router = Router()


class AddNotification(StatesGroup):
    minutes = State()
    title = State()


@router.message(F.text.lower().in_({"add reminder", "добавить напоминание"}))
async def add_notification(message: Message, state: FSMContext):
    lang = await ORM.select_user_language(user_id=message.from_user.id)
    await message.answer(strings[lang]['add_not'], reply_markup=notification_interval_kb())
    await state.set_state(AddNotification.minutes)


@router.message(F.text, AddNotification.minutes)
async def get_notification_minutes(message: Message, state: FSMContext):

    minutes = message.text.replace("m", "")
    if not minutes.isdigit():
        await message.answer('Введите кол-во минут без дополнительных символов:')
        return

    if not int(minutes) in range(1, 500):
        await message.answer('Введите значение в пределе от 1мин до 500мин:')
        return
    else:
        await message.answer('Введите текст, который будет приходить в уведомлении:',
                             reply_markup=types.ReplyKeyboardRemove())
        await state.update_data(minutes=minutes)
        await state.set_state(AddNotification.title)


@router.message(F.text, AddNotification.title)
async def get_notification_title(message: Message, state: FSMContext, bot: Bot):

    title_length = 50
    lang = await ORM.select_user_language(user_id=message.from_user.id)

    if len(message.text) > title_length:
        await message.answer("Ваше сообщение слишком длинное (>50 символов)")
        return

    data = await state.get_data()
    title = message.text
    minutes = data['minutes']
    notification = NotificationDTO(user_id=message.from_user.id,
                                   minutes=int(minutes),
                                   title=title,
                                   created_at=datetime.datetime.utcnow())
    not_id = await ORM.insert_notification(notification=notification)
    await state.clear()
    await message.answer(f"Уведомление сработает через {notification.minutes} минут с сообщением:\n"
                         f"{notification.title}", reply_markup=main_menu_kb(lang=lang))
    await ORM.update_running_session(RunningSessionDTO(user_id=message.from_user.id, notification_id=not_id,
                                                       created_at=datetime.datetime.utcnow()))
    await run_scheduler(minutes=int(minutes), title=title, bot=bot, user_id=message.from_user.id)
