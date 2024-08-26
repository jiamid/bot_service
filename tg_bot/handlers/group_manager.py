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
from aiogram.types import Message
from tg_bot.bot import telegram_router, bot
import random


# 状态机类，用于跟踪用户是否验证
class Verification(StatesGroup):
    waiting_for_verification = State()


async def check_if_group_chat(chat_id: int):
    try:
        chat = await bot.get_chat(chat_id)
        chat_type = chat.type
        if chat_type in ["group", "supergroup"]:
            print(f"聊天 {chat_id} 是一个群聊，类型为: {chat_type}")
            return True
        else:
            print(f"聊天 {chat_id} 不是群聊，类型为: {chat_type}")
            return False
    except Exception as e:
        print(f"无法获取聊天信息: {e}")
        return False


group_ids = set()


@telegram_router.message(Command("gid"))
async def update_group_id(message: Message) -> None:
    chat_id = message.chat.id
    is_group = await check_if_group_chat(chat_id)
    if is_group:
        await message.answer(f"GroupId:{chat_id}")
        group_ids.add(chat_id)
    else:
        await message.answer(f"Now Chat {chat_id} is Not Group")


async def gen_verify_question():
    a = random.randint(0, 10)
    b = random.randint(0, 10)
    c = a + b
    d = random.randint(c + 1, c + 10)
    e = random.randint(c - 10, c - 1)
    inline_keyboard = [
        InlineKeyboardButton(text=f"{d}", callback_data="verify_fail"),
        InlineKeyboardButton(text=f"{e}", callback_data="verify_fail"),
        InlineKeyboardButton(text=f"{c}", callback_data="verify_user"),
    ]
    random.shuffle(inline_keyboard)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[inline_keyboard])
    return keyboard, f'{a}+{b}=?'


async def send_verify_to_group(group_id, user_id, nickname):
    user_mention = f'<a href="tg://user?id={user_id}">@{nickname}</a>'
    keyboard, question = await gen_verify_question()
    message = f"{user_mention}请进行验证，否则你将会被移除群组。{question}"
    verify_message = await bot.send_message(group_id, message, parse_mode='html',
                                            reply_markup=keyboard)
    return verify_message


@telegram_router.chat_member()
async def on_user_join(chat_member: types.ChatMemberUpdated, state: FSMContext):
    user_id = chat_member.new_chat_member.user.id
    nickname = chat_member.new_chat_member.user.first_name
    group_id = chat_member.chat.id
    status = chat_member.new_chat_member.status
    if status != 'member':
        return

    verify_message = await send_verify_to_group(group_id, user_id, nickname)

    # 将用户状态设置为等待验证
    await state.set_state(Verification.waiting_for_verification)
    await state.update_data(
        user_id=user_id,
        group_id=group_id,
        message_id=verify_message.message_id
    )

    # 设置超时时间为10秒，10秒后检查用户是否验证
    await asyncio.sleep(60)
    # 检查用户是否验证
    current_state = await state.get_state()
    if current_state == Verification.waiting_for_verification.state:
        try:
            await bot.ban_chat_member(chat_id=group_id, user_id=user_id)
            await bot.send_message(user_id, "你已被移除群组，因为未通过验证。")
            await bot.unban_chat_member(chat_id=group_id, user_id=user_id)
            await verify_message.delete()
        except TelegramBadRequest:
            logger.error(f"无法移除用户 {user_id}，可能因为没有足够的权限。")
        await state.clear()


# 处理按钮点击事件
@telegram_router.callback_query(StateFilter(Verification.waiting_for_verification))
async def process_verification(callback_query: types.CallbackQuery, state: FSMContext):
    print(callback_query.data)
    if callback_query.data == 'verify_user':
        await bot.answer_callback_query(callback_query.id)
        # await bot.send_message(callback_query.from_user.id, "验证通过！欢迎加入群组！")
        data = await state.get_data()
        await bot.delete_message(chat_id=data['group_id'], message_id=data['message_id'])
        await state.clear()
