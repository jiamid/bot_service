#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :push_result.py
# @Time :2024/12/24 17:39
# @Author :Jiamid
from fastapi import APIRouter
from pydantic import BaseModel, Field
from commonts.base_model import BaseResponseModel
from commonts.storage_manager import click_task_manager

router = APIRouter()


class NewTaskResultModel(BaseModel):
    keyword: str = Field(default='')
    target: str = Field(default='')


@router.post("/push_result", response_model=BaseResponseModel)
async def push_result(task_result: NewTaskResultModel):
    click_task_manager.log_click(task_result.target, task_result.keyword)
    return BaseResponseModel()
