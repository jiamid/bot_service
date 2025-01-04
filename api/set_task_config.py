#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :set_task_config.py
# @Time :2024/01/04 19:39
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


@router.post("/set_task_config", response_model=TaskConfigRespModel)
async def set_task_config(new_task_config: TaskConfigModel):
    timer_task_storage.set_value("keywords", new_task_config.keywords, False)
    timer_task_storage.set_value("targets", new_task_config.targets)
    keywords = timer_task_storage.get_value("keywords", [])
    targets = timer_task_storage.get_value("targets", [])
    return TaskConfigRespModel(data=TaskConfigModel(keywords=keywords, targets=targets))
