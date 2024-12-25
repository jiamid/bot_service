#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :target_setting.py
# @Time :2024/12/23 17:13
# @Author :Jiamid
from tg_bot.bot import telegram_router
from tg_bot.handlers.base_list_storage_api import BaseListStorageApi
from commonts.storage_manager import timer_task_storage

target_api = BaseListStorageApi(timer_task_storage, 'targets', 'target')(telegram_router)
