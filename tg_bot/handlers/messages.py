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
from aiogram.types import Message
from tg_bot.bot import telegram_router
from commonts.util import to_escape_string
from commonts.storage_manager import proxy_manager
from commonts.doubao import DouBaoBot
import re


@telegram_router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    await message.answer(f"Your ID: {message.from_user.id},Chat ID: {message.chat.id}")


@telegram_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f'*Hello {to_escape_string(message.from_user.first_name)}*\n'
                         f'\n`画xxxxxx`'
                         f'\n`/help`'
                         f'\n\n', parse_mode='MarkdownV2')


@telegram_router.message(Command("help"))
async def cmd_start(message: Message) -> None:
    await message.answer(f'*Hello {to_escape_string(message.from_user.first_name)}*\n'
                         f'_Region:_\n'
                         f'{proxy_manager.get_keys_str()}\n'
                         f'\n`/list_keywords`'
                         f'\n`/add_keyword 关键字`'
                         f'\n`/del_keyword 关键字`'
                         f'\n`/join`'
                         f'\n`/exit`'
                         f'\n`/list_proxys`'
                         f'\n`/set_proxy 代理区域 代理链接`'
                         f'\n`/del_proxy 代理区域`'
                         f'\n\n', parse_mode='MarkdownV2')


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


@telegram_router.message(F.text.contains("画"))
async def handle_draw(message: Message):
    get_flag = await message.reply('Get')
    prompt = message.text
    doubao_bot = DouBaoBot()
    result = await doubao_bot.text_to_img(prompt)
    img = result.get('url')
    tips = result.get('tips')
    if img:
        await message.reply_photo(img)
    if tips:
        await message.reply(tips)
    await get_flag.delete()
