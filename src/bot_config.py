import enum

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from settings import settings


class BotCommands(enum.Enum):
    ADD_NOT = "add_not"
    LAUNCH_NOT = "launch_not"
    INFO = "info"


_NOTIFY_COMMANDS_EN: dict[str, str] = {
    "/" + BotCommands.ADD_NOT.value: 'Create reminder✏️',
    "/" + BotCommands.LAUNCH_NOT.value: 'Run the reminder🔔',
    "/" + BotCommands.INFO.value: 'Informationℹ️',
}


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in _NOTIFY_COMMANDS_EN.items()
    ]
    await bot.set_my_commands(main_menu_commands)

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
