import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from src.database import ORM
from src.keyboards import notification_list_kb, NotificationCallbackData, NotificationCBActions
from src.models import RunningSessionDTO
from src.sheduler import run_scheduler
from src.strings import strings

router = Router()


@router.message(F.text.lower().in_({'запустить из списка', 'run from list'}))
async def show_notifications(message: Message):
    notifications = await ORM.select_user_notifications(user_id=message.from_user.id)
    lang = await ORM.select_user_language(user_id=message.from_user.id)
    if notifications:
        await message.answer(text=strings[lang]['not_show'],
                             reply_markup=notification_list_kb(notifications=notifications))
        return
    await message.answer(text='Добавьте напоминание.')


@router.callback_query(NotificationCallbackData.filter())
async def launch_notification(callback: CallbackQuery, callback_data: NotificationCallbackData,
                              bot: Bot):

    not_id = callback_data.not_id

    if callback_data.action == NotificationCBActions.SHOW:

        notification = await ORM.select_notification_by_id(not_id)
        await ORM.update_running_session(session=RunningSessionDTO(user_id=callback.from_user.id,
                                                                   notification_id=not_id,
                                                                   created_at=datetime.datetime.utcnow()))
        await callback.answer()
        await run_scheduler(minutes=notification.minutes, title=notification.title, bot=bot,
                            user_id=callback.from_user.id)

    elif callback_data.action == NotificationCBActions.DELETE:
        await ORM.delete_notification_by_id(not_id=not_id)
        notifications = await ORM.select_user_notifications(user_id=callback.from_user.id)
        await callback.message.edit_reply_markup(reply_markup=notification_list_kb(notifications=notifications))
        await callback.answer()


@router.message(F.text.lower().in_({"остановить текущее напоминание", "stop the current reminder"}))
async def kill_running_session(message: Message):
    current_session = await ORM.get_running_session(user_id=message.from_user.id)
    lang = await ORM.select_user_language(user_id=message.from_user.id)
    if not current_session:
        await message.answer(strings[lang]['no_in_run'])
        return
    notification = await ORM.select_notification_by_id(not_id = current_session.notification_id)
    await ORM.kill_running_session(user_id=message.from_user.id)
    await message.answer(text=strings[lang]['stop_not'].format(notification.minutes, notification.title))
