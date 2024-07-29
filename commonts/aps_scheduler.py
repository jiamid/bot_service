# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 11:28
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : aps_scheduler.py
# @Software: PyCharm
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# 为SQLAlchemy 定义数据库url地址
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://:halo@api.jiamid.com:5432/jiamid'

scheduler = AsyncIOScheduler({
    'apscheduler.jobstores.default': {
        'type': 'sqlalchemy',
        'url': SQLALCHEMY_DATABASE_URI,
        'tablename': 'task_job'
    },
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20'
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '10'
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '10',
    'apscheduler.timezone': 'Asia/Shanghai',  # 设置时区
})