#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :set_task_config.py
# @Time :2024/01/04 19:39
# @Author :Jiamid
from fastapi import APIRouter, Request
from commonts.storage_manager import timer_task_storage
from commonts.base_model import BaseResponseModel
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()


class TaskConfigModel(BaseModel):
    keywords: list[str] = Field(default=[])
    targets: list[str] = Field(default=[])


class TaskConfigRespModel(BaseResponseModel):
    data: TaskConfigModel = Field(default=TaskConfigModel())


@router.post("/set_task_config", response_model=TaskConfigRespModel)
async def set_task_config(new_task_config: TaskConfigModel, sign: str):
    if sign != 'jiamid':
        return TaskConfigRespModel(code=403, msg='Error')
    timer_task_storage.set_value("click_keywords", new_task_config.keywords, False)
    timer_task_storage.set_value("targets", new_task_config.targets)
    keywords = timer_task_storage.get_value("click_keywords", [])
    targets = timer_task_storage.get_value("targets", [])
    return TaskConfigRespModel(data=TaskConfigModel(keywords=keywords, targets=targets))


templates = Jinja2Templates(directory='templates')


@router.get("/set_task_config", response_class=HTMLResponse)
async def set_task_config_html(request: Request):
    return templates.TemplateResponse('set_task_config_page.html', {'request': request})
