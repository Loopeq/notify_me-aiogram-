import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from logger_config import logger
from src.database import ORM
from src.keyboards import notification_list_kb, NotificationCallbackData
from src.models import RunningSessionDTO
from src.sheduler import run_scheduler

router = Router()


@router.message(F.text.lower().in_({'запустить из списка', 'run from list'}))
async def show_notifications(message: Message):
    logger.info("Here")
    notifications = await ORM.select_user_notifications(user_id=message.from_user.id)
    await message.answer(text="Веберите нужное напоминание",
                         reply_markup=notification_list_kb(notifications=notifications))


@router.callback_query(NotificationCallbackData.filter())
async def launch_notification(callback: CallbackQuery, callback_data: NotificationCallbackData,
                              bot: Bot):

    not_id = callback_data.not_id
    notification = await ORM.select_notification_by_id(not_id)
    await ORM.update_running_session(session=RunningSessionDTO(user_id=callback.from_user.id,
                                                               notification_id=not_id,
                                                               created_at=datetime.datetime.utcnow()))
    await callback.answer()
    await run_scheduler(minutes=notification.minutes, title=notification.title, bot=bot,
                        user_id=callback.from_user.id)


@router.message(F.text.lower().in_({"остановить текущее напоминание", "stop the current reminder"}))
async def kill_running_session(message: Message):
    current_session = await ORM.get_running_session(user_id=message.from_user.id)
    if not current_session:
        await message.answer('У вас не запущено ни одно напоминание')
        return
    await ORM.kill_running_session(user_id=message.from_user.id)


