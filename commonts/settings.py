# -*- coding: utf-8 -*-
# @Time    : 2024/7/19 17:29
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : settings.py
# @Software: PyCharm
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.prod.env', '.dev.env'),  # first search .dev.env, then .prod.env
        env_file_encoding='utf-8')

    debug: bool = True
    bot_token: str = '1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base_webhook_url: str = 'https://my.host.name'
    webhook_path: str = '/path/to/webhook'
    secret_token: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Additional security token for webhook
    doubao_ak: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Additional security token for webhook
    doubao_sk: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Additional security token for webhook


settings = Settings()
