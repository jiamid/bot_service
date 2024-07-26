# -*- coding: utf-8 -*-
# @Time    : 2024/7/26 17:18
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : messages.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
from loguru import logger
from aiogram import types
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.types import Message
from tg_bot.bot import telegram_router


@telegram_router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    await message.answer(f"Your ID: {message.from_user.id}")


@telegram_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@telegram_router.message(F.text == "echo")
async def echo(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try!")


@telegram_router.message(F.text == "ping")
async def hello(message: types.Message) -> None:
    try:
        await message.answer("pong")
    except Exception as e:
        logger.error(f"Can't send message - {e}")
        await message.answer("Nice try!")