# -*- coding: utf-8 -*-
# @Time    : 2024/7/19 17:24
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : main.py
# @Software: PyCharm
from fastapi import FastAPI
from loguru import logger
from commonts.logger import init_logging
from commonts.settings import settings
from tg_bot.bot import bot
from uvicorn import run
from contextlib import asynccontextmanager
from commonts.scheduler_manager import scheduler_manager
from api import router


async def init_scheduler():
    logger.info("🚀 Starting scheduler")
    scheduler_manager.run()


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("🚀 Starting application")
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != f'{settings.base_webhook_url}{settings.webhook_path}':
        logger.info(f'set webhook {settings.webhook_path}')
        await bot.set_webhook(
            url=f'{settings.base_webhook_url}{settings.webhook_path}',
            secret_token=settings.secret_token,
            drop_pending_updates=True,
            max_connections=100,
        )
    await init_scheduler()
    yield
    logger.info("⛔ Stopping application")


app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == '__main__':
    init_logging()
    logger.info("bot start")
    run(app, host='0.0.0.0', port=9999)
