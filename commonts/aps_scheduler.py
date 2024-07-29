# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 11:28
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : aps_scheduler.py
# @Software: PyCharm
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler({
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '10'
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '10',
    'apscheduler.timezone': 'Asia/Shanghai',  # 设置时区
})
