# -*- coding: utf-8 -*-
# @Time    : 2024/7/26 17:12
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : bot.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, Router
from commonts.settings import settings

bot = Bot(token=settings.bot_token)

telegram_router = Router(name="telegram")
dp = Dispatcher()
dp.include_router(telegram_router)
