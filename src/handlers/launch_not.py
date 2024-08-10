import datetime
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from src.database import ORM
from src.keyboards import notification_list_kb, NotificationCallbackData, NotificationCBActions, \
    kill_running_notification_button, ProcessKillerCallbackData
from src.models import RunningSessionDTO
from src.sheduler import run_scheduler
from src.strings import strings
from ..bot_config import BotCommands


router = Router()


@router.message(Command(BotCommands.LAUNCH_NOT.value))
async def show_notifications(message: Message):
    notifications = await ORM.select_user_notifications(user_id=message.from_user.id)
    lang = await ORM.select_user_language(user_id=message.from_user.id)
    if notifications:
        await message.answer(text=strings[lang]['not_show'],
                             reply_markup=notification_list_kb(notifications=notifications))
        return
    await message.answer(text=f"{strings[lang]['nothing_to_launch']} \n\n /{BotCommands.ADD_NOT.value}")


@router.callback_query(NotificationCallbackData.filter())
async def launch_notification(callback: CallbackQuery, callback_data: NotificationCallbackData,
                              bot: Bot):

    not_id = callback_data.not_id
    if callback_data.action == NotificationCBActions.SHOW:

        notification = await ORM.select_notification_by_id(not_id)
        await ORM.update_running_session(session=RunningSessionDTO(user_id=callback.from_user.id,
                                                                   notification_id=not_id,
                                                                   created_at=datetime.datetime.utcnow()))
        message = await bot.send_message(chat_id=callback.from_user.id,
                                         text=f'🔔Запущено - [{notification.minutes}m - {notification.title}]')
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=message.message_id,
                                            reply_markup=kill_running_notification_button(message_id=message.message_id))
        await bot.pin_chat_message(chat_id=callback.from_user.id, message_id=message.message_id,
                                   disable_notification=False)
        await callback.answer()

        await run_scheduler(minutes=notification.minutes, title=notification.title, bot=bot,
                            user_id=callback.from_user.id)

    elif callback_data.action == NotificationCBActions.DELETE:
        await ORM.delete_notification_by_id(not_id=not_id)
        notifications = await ORM.select_user_notifications(user_id=callback.from_user.id)
        await callback.message.edit_reply_markup(reply_markup=notification_list_kb(notifications=notifications))
        await callback.answer()


@router.callback_query(ProcessKillerCallbackData.filter())
async def kill_running_session(callback: CallbackQuery, callback_data: ProcessKillerCallbackData,
                               bot: Bot):
    current_session = await ORM.get_running_session(user_id=callback.from_user.id)
    lang = await ORM.select_user_language(user_id=callback.from_user.id)
    if not current_session:
        await callback.message.answer(strings[lang]['no_in_run'])
        return
    message_id = callback_data.message_id
    await bot.unpin_all_chat_messages(chat_id=callback.from_user.id)
    notification = await ORM.select_notification_by_id(not_id=current_session.notification_id)
    await ORM.kill_running_session(user_id=callback.from_user.id)
    await callback.message.answer(text=strings[lang]['stop_not'].format(notification.minutes, notification.title))
    await bot.delete_message(chat_id=callback.from_user.id, message_id=message_id)
    await callback.answer()
