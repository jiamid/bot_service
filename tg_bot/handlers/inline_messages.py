# -*- coding: utf-8 -*-
# @Time    : 2024/8/26 17:18
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : inline_messages.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
from aiogram.filters import Command
from loguru import logger
from aiogram import types
from tg_bot.bot import telegram_router, bot
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest
import asyncio
from aiogram.filters.state import State, StatesGroup


@telegram_router.message(Command("t"))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="点击我！", callback_data="button_click")]
    ])
    await message.answer("点击下方的按钮：", reply_markup=keyboard)


# 处理按钮点击
@telegram_router.callback_query(lambda c: c.data == 'button_click')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "你点击了按钮！")
