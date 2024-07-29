# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 12:15
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : tasks.py
# @Software: PyCharm
from loguru import logger
from aiogram import types
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.types import Message
from tg_bot.bot import telegram_router, bot
from commonts.aps_scheduler import scheduler
from datetime import datetime, timedelta

chat_ids = []


@telegram_router.message(Command("join"))
async def join_team(message: Message) -> None:
    chat_ids.append(message.chat.id)
    await message.answer(f"Your ID: {message.from_user.id}")

async def send_tg():
    for x in chat_ids:
        logger.info(f'send message to {x}')
        await bot.send_message(x, 'this is a test')


@telegram_router.message(Command("start1"))
async def start_task(message: Message) -> None:
    scheduler.add_job(send_tg, id='task4', trigger='interval', minutes=10,
                      next_run_time=datetime.now() + timedelta(seconds=10)
                      )

    await message.answer(f"start success")



