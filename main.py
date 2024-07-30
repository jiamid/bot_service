# -*- coding: utf-8 -*-
# @Time    : 2024/7/19 17:24
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : main.py
# @Software: PyCharm
from fastapi import FastAPI, Header
from loguru import logger
from commonts.logger import init_logging
from commonts.settings import settings
from tg_bot.bot import bot, dp
from typing import Annotated
from uvicorn import run
from aiogram import types
from contextlib import asynccontextmanager
from tg_bot import handlers
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


@app.post(settings.webhook_path)
async def bot_webhook(update: dict,
                      x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None) -> None | dict:
    """ Register webhook endpoint for telegram bot"""
    if x_telegram_bot_api_secret_token != settings.secret_token:
        logger.error(f"Wrong secret token ! {x_telegram_bot_api_secret_token}")
        return {"status": "error", "message": "Wrong secret token !"}
    telegram_update = types.Update(**update)
    await dp.feed_webhook_update(bot=bot, update=telegram_update)



if __name__ == '__main__':
    init_logging()
    logger.info("bot start")
    run(app, host='0.0.0.0', port=9999)
