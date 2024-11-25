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
from commonts.storage_manager import iptable_storage


@telegram_router.message(Command("list_ip"))
async def list_ip(message: Message) -> None:
    try:
        white_ips = iptable_storage.get_value('white', [])
        k_str = '\n'.join(white_ips)
        text = f"White:\n{k_str}"
        await message.answer(text)
    except Exception as e:
        print(e)
        logger.error(f'list ip fail')
        await message.answer('list ip error')


@telegram_router.message(Command("add_ip"))
async def add_ip(message: Message) -> None:
    try:
        args = message.text.split()[1:]
        ip = args[0]
        pw = args[-1]
        if pw != 'jiamid':
            await message.answer('password error')
        else:
            iptable_storage.add_to_key('white', ip)
            text = f"add ip:{ip} success"
            logger.info(text)
            await message.answer(text)
    except Exception as e:
        print(e)
        logger.error(f'add ip fail')
        await message.answer('add ip error,check arg')


@telegram_router.message(Command("del_ip"))
async def del_ip(message: Message) -> None:
    try:
        args = message.text.split()[1:]
        ip = args[0]
        iptable_storage.del_from_key('white', ip)
        text = f"del ip:{ip} success"
        logger.info(text)
        await message.answer(text)
    except:
        logger.error(f'del ip fail')
        await message.answer('add ip error,check arg')


