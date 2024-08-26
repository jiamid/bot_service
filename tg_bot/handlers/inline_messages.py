# -*- coding: utf-8 -*-
# @Time    : 2024/8/26 17:18
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : inline_messages.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
from aiogram import types
from aiogram.types import Message,InlineKeyboardButton,InlineKeyboardMarkup
from tg_bot.bot import telegram_router,bot



@telegram_router.message(commands=['t'])
async def send_welcome(message: types.Message):
    # 创建一个按钮
    button = InlineKeyboardButton(text="点击我", callback_data="button_click")

    # 创建一个 InlineKeyboardMarkup 对象，并添加按钮
    keyboard = InlineKeyboardMarkup().add(button)

    # 发送带有按钮的消息
    await message.reply("这是一个带有按钮的消息：", reply_markup=keyboard)


# 处理按钮点击
@telegram_router.callback_query_handler(lambda c: c.data == 'button_click')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "你点击了按钮！")
