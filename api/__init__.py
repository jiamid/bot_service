# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 15:19
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : __init__.py.py
# @Software: PyCharm
from fastapi import APIRouter
from api.gen_index import router as index_router
from api.gen_ad_result import router as result_router
from api.bot_webhook import router as bot_router

router = APIRouter()
router.include_router(index_router)
router.include_router(result_router)
router.include_router(bot_router)
