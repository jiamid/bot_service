#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :target_setting.py
# @Time :2024/12/23 17:13
# @Author :Jiamid
from loguru import logger
from aiogram.filters import Command
from aiogram.types import Message
from tg_bot.bot import telegram_router
from commonts.storage_manager import timer_task_storage


@telegram_router.message(Command("list_targets"))
async def list_targets(message: Message) -> None:
    try:
        data = timer_task_storage.get_value('targets', [])
        _str = '\n'.join(data)
        text = f"Targets:\n{_str}"
        await message.answer(text)
    except Exception as e:
        print(e)
        logger.error(f'list targets fail')
        await message.answer('list targets error')


@telegram_router.message(Command("add_target"))
async def add_target(message: Message) -> None:
    try:
        args = message.text.split()[1:]
        data = args[0]
        timer_task_storage.add_to_key('targets', data)
        text = f"add Target:{data} success"
        logger.info(text)
        await message.answer(text)
    except Exception as e:
        print(e)
        logger.error(f'add target fail')
        await message.answer('add target error,check arg')


@telegram_router.message(Command("del_target"))
async def del_target(message: Message) -> None:
    try:
        args = message.text.split()[1:]
        data = args[0]
        timer_task_storage.del_from_key('targets', data)
        text = f"del Target:{data} success"
        logger.info(text)
        await message.answer(text)
    except:
        logger.error(f'del target fail')
        await message.answer('add target error,check arg')
