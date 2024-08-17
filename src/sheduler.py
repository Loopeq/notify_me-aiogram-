import asyncio
import datetime
import math

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.database import ORM
from src.models import SessionTimeDeltaDTO


async def send_notification(user_id: int,
                            message: str,
                            not_id: int,
                            minutes: int,
                            bot: Bot):
    await ORM.update_session_time_delta(SessionTimeDeltaDTO(
        user_id=user_id, notification_id=not_id, minutes=minutes,
        created_at=datetime.datetime.utcnow()))
    delta_minutes = await ORM.select_session_time_delta(user_id, not_id)
    await bot.send_message(chat_id=user_id, text=f"🔔 {message} - [{format_minutes(delta_minutes)}]")


def format_minutes(minutes: int):
    if minutes >= 60:
        return f"{math.ceil(minutes / 60)} ч."
    return f"{minutes} мин."


async def run_scheduler(minutes: int, title: str, bot: Bot, user_id: int, not_id: int):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_notification, 'interval', minutes=minutes, args=(user_id, title, not_id,
                                                                            minutes, bot))
    scheduler.start()

    while True:
        current_session = await ORM.get_running_session(user_id=user_id)
        if not current_session:
            scheduler.shutdown()
            break
        await asyncio.sleep(1)




