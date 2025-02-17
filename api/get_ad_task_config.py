#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :get_task_config.py
# @Time :2024/12/23 15:39
# @Author :Jiamid
from fastapi import APIRouter
from commonts.storage_manager import timer_task_storage, proxys_storage
from commonts.base_model import BaseResponseModel
from pydantic import BaseModel, Field

router = APIRouter()


class TaskConfigModel(BaseModel):
    keywords: list[str] = Field(default=[])
    proxies: dict[str,str] = Field(default={})


class TaskConfigRespModel(BaseResponseModel):
    data: TaskConfigModel = Field(default=TaskConfigModel())


@router.get("/get_ad_task_config", response_model=TaskConfigRespModel)
async def get_ad_task_config():
    keywords = timer_task_storage.get_value("keywords", [])
    proxies = proxys_storage.data
    return TaskConfigRespModel(data=TaskConfigModel(keywords=keywords, proxies=proxies))
