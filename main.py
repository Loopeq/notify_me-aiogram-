import asyncio

from src.bot_config import bot, dp
from src.database import ORM
from src.handlers.common import router as common_router
from src.handlers.add_not import router as add_not
from src.handlers.launch_not import router as launch_not


async def main():

    await ORM.setup()

    dp.include_routers(common_router, add_not, launch_not)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
