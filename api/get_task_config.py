#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :get_task_config.py
# @Time :2024/12/23 15:39
# @Author :Jiamid
from fastapi import APIRouter
from commonts.storage_manager import timer_task_storage
from commonts.base_model import BaseResponseModel
from pydantic import BaseModel, Field

router = APIRouter()


class TaskConfigModel(BaseModel):
    keywords: list[str] = Field(default=[])
    targets: list[str] = Field(default=[])


class TaskConfigRespModel(BaseResponseModel):
    data: TaskConfigModel = Field(default=TaskConfigModel())


@router.get("/get_task_config", response_model=TaskConfigRespModel)
async def get_task_config():
    keywords = timer_task_storage.get_value("click_keywords", [])
    targets = timer_task_storage.get_value("targets", [])
    return TaskConfigRespModel(data=TaskConfigModel(keywords=keywords, targets=targets))
