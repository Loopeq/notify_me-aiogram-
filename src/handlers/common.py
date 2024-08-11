import datetime

from aiogram import Router, types, Bot
from aiogram.filters import CommandStart, Command

from aiogram.types import Message
from ..bot_config import set_main_menu, BotCommands
from src.database import ORM
from src.keyboards import LanguageCallbackData, select_language_kb
from src.models import UserDTO
from src.strings import strings

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    await set_main_menu(bot=bot)
    await message.answer(text=strings['common']['select_lang'],
                         reply_markup=select_language_kb())


@router.message(Command(BotCommands.INFO.value))
async def cmd_info(message: Message):
    lang = await ORM.select_user_language(user_id=message.from_user.id)
    await message.answer(f'@indigridient - {strings[lang]["contact"]}')


@router.callback_query(LanguageCallbackData.filter())
async def create_user_config(callback: types.CallbackQuery, callback_data: LanguageCallbackData):
    user = UserDTO(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        language=callback_data.value,
        created_at=datetime.datetime.utcnow()
    )

    await ORM.insert_user_config(user=user)

    await callback.message.answer(text=f"{user.username.strip().title()}, "
                                       f"{strings[user.language]['greeting']} \n\n {''*20}/{BotCommands.ADD_NOT.value}")
    await callback.answer()

