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


@telegram_router.message(Command("list_click_log"))
async def list_click_log(message: Message) -> None:
    try:
        data = click_task_manager.log_list
        if data:
            _str = '\n'.join(data)
            text = f"日志:\n{_str}"
        else:
            text = f"暂无日志"
        await message.answer(text)
    except Exception as e:
        logger.error(f'list click log fail e: {e}')
        await message.answer('list click log error')


@telegram_router.message(Command("list_click_result"))
async def list_click_result(message: Message) -> None:
    try:
        data = click_task_manager.data.data
        if data:
            _str = '\n'.join([f'[{k}]({v})' for k, v in data.items()])
            text = f"点击情况:\n{_str}"
        else:
            text = f"暂无点击"
        await message.answer(text)
    except Exception as e:
        logger.error(f'list click result fail e: {e}')
        await message.answer('list click result error')


@telegram_router.message(Command("del_click_result"))
async def del_click_result(message: Message) -> None:
    try:
        args = message.text.split()[1:]
        if args:
            target = args[0]
            click_task_manager.remove(target)
            text = f'已删除：{target}'
        else:
            click_task_manager.remove_all()
            text = f'已删除所有'
        await message.answer(text)
    except Exception as e:
        logger.error(f'del click result fail e: {e}')
        await message.answer('del click result error')
