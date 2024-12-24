#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :click_result_manager.py
# @Time :2024/12/24 23:46
# @Author :Jiamid
from loguru import logger
from aiogram.filters import Command
from aiogram.types import Message
from tg_bot.bot import telegram_router
from commonts.storage_manager import click_task_manager


@telegram_router.message(Command("list_click_result"))
async def list_click_result(message: Message) -> None:
    try:
        data = click_task_manager.log_list
        _str = '\n'.join(data)
        text = f"点击情况:\n{_str}"
        await message.answer(text)
    except Exception as e:
        logger.error(f'list click result fail e: {e}')
        await message.answer('list click result error')

