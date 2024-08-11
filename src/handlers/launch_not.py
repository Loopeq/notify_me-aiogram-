import datetime
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from src.database import ORM
from src.keyboards import notification_list_kb, NotificationCallbackData, NotificationCBActions, \
    kill_running_notification_button, ProcessKillerCallbackData
from src.models import RunningSessionDTO, NotificationDTO
from src.sheduler import run_scheduler
from src.strings import strings
from ..bot_config import BotCommands

router = Router()


async def run_notification(bot: Bot,
                           user_id: int,
                           not_id: int,
                           notification: NotificationDTO):
    can_be_running = await ORM.update_running_session(session=RunningSessionDTO(user_id=user_id,
                                                                                notification_id=not_id,
                                                                                created_at=datetime.datetime.utcnow()))
    lang = await ORM.select_user_language(user_id)
    if not can_be_running:
        await bot.send_message(chat_id=user_id,
                               text=strings[lang]['session_count_expt'])
        return

    message = await bot.send_message(chat_id=user_id,
                                     text=f'{strings[lang]["launched"]} - [{notification.minutes}m - {notification.title}]')
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=message.message_id,
                                        reply_markup=kill_running_notification_button(message_id=message.message_id,
                                                                                      not_id=not_id))
    await bot.pin_chat_message(chat_id=user_id, message_id=message.message_id,
                               disable_notification=False)

    await run_scheduler(minutes=notification.minutes, title=notification.title, bot=bot,
                        user_id=user_id)


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

        await callback.answer()

        await run_notification(bot=bot, user_id=callback.from_user.id,
                               not_id=not_id, notification=notification)
    elif callback_data.action == NotificationCBActions.DELETE:
        await ORM.delete_notification_by_id(not_id=not_id)
        notifications = await ORM.select_user_notifications(user_id=callback.from_user.id)
        await callback.message.edit_reply_markup(reply_markup=notification_list_kb(notifications=notifications))
        await callback.answer()


@router.callback_query(ProcessKillerCallbackData.filter())
async def kill_running_session(callback: CallbackQuery, callback_data: ProcessKillerCallbackData,
                               bot: Bot):
    lang = await ORM.select_user_language(user_id=callback.from_user.id)
    message_id = callback_data.message_id
    notification_id = callback_data.not_id
    await bot.unpin_chat_message(chat_id=callback.from_user.id,
                                 message_id=message_id)
    notification = await ORM.select_notification_by_id(not_id=notification_id)
    await ORM.kill_running_session(notification_id=notification_id)
    await callback.message.answer(text=strings[lang]['stop_not'].format(notification.minutes, notification.title))
    await bot.delete_message(chat_id=callback.from_user.id, message_id=message_id)
    await callback.answer()
