# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 16:04
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : task_setting.py
# @Software: PyCharm
from loguru import logger
from aiogram.filters import Command
from aiogram.types import Message
from tg_bot.bot import telegram_router
from commonts.storage_manager import timer_task_storage
from commonts.scheduler_manager import scheduler_manager
from tg_bot.handlers.timer_scan import do_scan


@telegram_router.message(Command("list_keywords"))
async def list_keywords(message: Message) -> None:
    try:
        keywords = timer_task_storage.get_value('keywords', [])
        k_str = '\n'.join(keywords)
        text = f"Keywords:\n{k_str}"
        await message.answer(text)
    except Exception as e:
        print(e)
        logger.error(f'list keyword fail')
        await message.answer('list keyword error')


@telegram_router.message(Command("add_keyword"))
async def add_keyword(message: Message) -> None:
    try:
        args = message.text.split()[1:]
        keyword = args[0]
        timer_task_storage.add_to_key('keywords', keyword)
        text = f"add Keyword:{keyword} success"
        logger.info(text)
        await message.answer(text)
    except Exception as e:
        print(e)
        logger.error(f'add keyword fail')
        await message.answer('add keyword error,check arg')


@telegram_router.message(Command("del_keyword"))
async def del_keyword(message: Message) -> None:
    try:
        args = message.text.split()[1:]
        keyword = args[0]
        timer_task_storage.del_from_key('keywords', keyword)
        text = f"del Keyword:{keyword} success"
        logger.info(text)
        await message.answer(text)
    except:
        logger.error(f'del keyword fail')
        await message.answer('add keyword error,check arg')


@telegram_router.message(Command("set_sem"))
async def set_sem(message: Message) -> None:
    try:
        args = message.text.split()[1:]
        sem_str = args[0]
        sem = int(sem_str)
        if sem < 1:
            raise ValueError('sem must > 1')
        timer_task_storage.set_value('sem', sem)
        text = f"set sem:{sem} success"
        logger.info(text)
        await message.answer(text)
    except Exception as e:
        print(e)
        logger.error(f'set sem fail')
        await message.answer('set sem fail only num and > 1')


@telegram_router.message(Command("join"))
async def join_team(message: Message) -> None:
    timer_task_storage.add_to_key('chat_ids', message.chat.id)
    logger.info(f'{message.chat.id} join success')
    await message.answer("Success to join")
    status = scheduler_manager.add_task(do_scan, 'timer_scan')
    if status:
        logger.info(f'timer_scan start success by {message.chat.id}')
        await message.answer("Start timer_scan")


@telegram_router.message(Command("exit"))
async def exit_item(message: Message) -> None:
    timer_task_storage.del_from_key('chat_ids', message.chat.id)
    logger.info(f'{message.chat.id} exit success')
    await message.answer("Success to exit")
    chat_ids = timer_task_storage.get_value('chat_ids', [])
    if not chat_ids:
        remove_status = scheduler_manager.remove_task('timer_scan')
        if remove_status:
            await message.answer("Remove timer_scan success")
            logger.info(f'timer_scan remove success')
        else:
            await message.answer("Remove timer_scan fail")
            logger.info(f'timer_scan remove fail')
