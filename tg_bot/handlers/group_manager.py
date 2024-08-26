# -*- coding: utf-8 -*-
# @Time    : 2024/8/26 14:27
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : group_manager.py
# @Software: PyCharm
from loguru import logger
from aiogram import types
from aiogram.filters import StateFilter, ChatMemberUpdatedFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated
from aiogram.exceptions import TelegramBadRequest
import asyncio
from tg_bot.bot import telegram_router, bot


# 状态机类，用于跟踪用户是否验证
class Verification(StatesGroup):
    waiting_for_verification = State()


# 处理新成员加入的事件
# @telegram_router.message(Command("t1"))
# async def on_user_join(event: types.Message, state: FSMContext):

@telegram_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=['member']))
async def on_user_join(chat_member: types.ChatMemberUpdated, state: FSMContext):
    user_id = chat_member.new_chat_member.user.id
    group_id = chat_member.chat.id
    status = chat_member.new_chat_member.status

    print(f"用户 {user_id} 在群组 {group_id} 的状态更新为: {status}")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="点击验证", callback_data="verify_user")]
    ])

    await bot.send_message(user_id, "请点击下方按钮进行验证，否则你将会被移除群组。", reply_markup=keyboard)

    # 将用户状态设置为等待验证
    await state.set_state(Verification.waiting_for_verification)
    await state.update_data(user_id=user_id)

    # 设置超时时间为60秒，60秒后检查用户是否验证
    await asyncio.sleep(10)

    # 检查用户是否验证
    current_state = await state.get_state()
    if current_state == Verification.waiting_for_verification.state:
        try:
            await bot.ban_chat_member(chat_id=group_id, user_id=user_id)
            await bot.send_message(user_id, "你已被移除群组，因为未通过验证。")
        except TelegramBadRequest:
            logger.error(f"无法移除用户 {user_id}，可能因为没有足够的权限。")
        await state.clear()


# 处理按钮点击事件
@telegram_router.callback_query(StateFilter(Verification.waiting_for_verification))
async def process_verification(callback_query: types.CallbackQuery, state: FSMContext):
    print(callback_query.data)
    if callback_query.data == 'verify_user':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "验证通过！欢迎加入群组！")
        await state.clear()


