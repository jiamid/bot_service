# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 16:04
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : proxy_setting.py
# @Software: PyCharm
from loguru import logger
from aiogram.filters import Command
from aiogram.types import Message
from tg_bot.bot import telegram_router
from commonts.storage_manager import proxys_storage, proxy_manager


@telegram_router.message(Command("list_proxys"))
async def list_proxys(message: Message) -> None:
    try:
        data = proxys_storage.data
        k_str = '\n'.join([f'【{k}】{v}' for k, v in data.items()])
        text = f"Proxys:\n{k_str}"
        await message.answer(text)
    except Exception as e:
        print(e)
        logger.error(f'list proxy fail')
        await message.answer('list proxy error')


@telegram_router.message(Command("set_proxy"))
async def set_proxy(message: Message) -> None:
    try:
        args = message.text.split()[1:]
        region = args[0]
        proxy = args[1]
        proxys_storage.set_value(region, proxy)
        proxy_manager.refresh_proxy()
        text = f"set proxy {region} {proxy} success"
        logger.info(text)
        await message.answer(text)
    except Exception as e:
        print(e)
        logger.error(f'add keyword fail')
        await message.answer('add keyword error,check arg')


@telegram_router.message(Command("del_proxy"))
async def del_proxy(message: Message) -> None:
    try:
        args = message.text.split()[1:]
        region = args[0]
        proxys_storage.del_key(region)
        text = f"del proxy:{region} success"
        logger.info(text)
        await message.answer(text)
    except Exception as e:
        print(e)
        logger.error(f'del proxy fail')
        await message.answer('del proxy error')
