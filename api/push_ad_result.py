#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :push_result.py
# @Time :2024/12/24 17:39
# @Author :Jiamid
import datetime
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel, Field
from commonts.base_model import BaseResponseModel
from tg_bot.handlers.timer_scan import decimal_to_base36
from commonts.json_manager import json_manager
from commonts.storage_manager import history_html_storage
from commonts.settings import settings
from tg_bot.bot import send_message_to_bot
from commonts.storage_manager import timer_task_storage

router = APIRouter()


class NewAdResultModel(BaseModel):
    keyword: str = Field(default='')
    os: str = Field(default='')
    region: str = Field(default='')
    domain: str = Field(default='')
    create_at: str = Field(default='')


class NewAdResultReqModel(BaseModel):
    data: List[NewAdResultModel] = Field(default=[])

    def get_data_json_dict(self):
        result = []
        for ad_result in self.data:
            result.append(ad_result.model_dump())
        return result


async def push_ad_result(ad_result: NewAdResultReqModel):
    now = datetime.datetime.now()
    now_ts = int(now.timestamp())
    ts_id = decimal_to_base36(now_ts)
    filename = f'r{ts_id}'
    json_manager.save_file(ad_result.get_data_json_dict(), filename)
    history_list: list = history_html_storage.get_value('history', [])
    history_list.append({now.strftime('%Y-%m-%d %H:%M:%S'): filename})
    history_list = history_list[-50:]
    history_html_storage.set_value('history', history_list)
    text = f'访问以下网站查看结果\n{settings.base_webhook_url}/r/{filename}'
    chat_ids = timer_task_storage.get_value('chat_ids', [])
    for chat_id in chat_ids:
        await send_message_to_bot(chat_id, text)
    return BaseResponseModel()