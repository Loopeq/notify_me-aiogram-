import asyncio

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.database import ORM


async def send_notification(bot: Bot, user_id: int, message: str):
    await bot.send_message(chat_id=user_id, text=f"🔔 {message}")


async def run_scheduler(minutes: int, title: str, bot: Bot, user_id: int):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_notification, 'interval', seconds=minutes, args=(bot, user_id, title))
    scheduler.start()

    while True:
        current_session = await ORM.get_running_session(user_id=user_id)
        if not current_session:
            scheduler.shutdown()
            break
        await asyncio.sleep(1)




