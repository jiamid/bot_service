# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 14:28
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : timer_scan.py
# @Software: PyCharm
from commonts.async_task_manager import AsyncTaskManager
from tg_bot.bot import bot
from commonts.storage_manager import timer_task_storage
from commonts.storage_manager import proxy_manager
from commonts.storage_manager import history_html_storage
from commonts.json_manager import json_manager
from commonts.util import to_escape_string
from commonts.search import Google
from loguru import logger
import asyncio
from datetime import datetime
import itertools


async def send_message_to_bot(chat_id, text, parse_mode=None):
    flag = True
    times = 1
    while flag and times < 3:
        try:
            await bot.send_message(chat_id, text=text, parse_mode=parse_mode)
            flag = False
        except Exception as e:
            logger.error(f'send message fail {times} e:{e}')
            times += 1
            await asyncio.sleep(1)


os_map = {
    0: None,
    1: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.59 Safari/537.36',
    2: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    3: 'Mozilla/5.0 (Linux; Android  11; Pixel 5a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.9 Mobile Safari/537.36',
    4: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.59 Safari/537.36',
}
os_name_map = {
    1: 'WIN',
    2: 'IOS',
    3: 'ANDROID',
    4: 'MAC',
}


async def scan_one(keyword: str, os: int, region: str, chat_ids: list,
                   result_list: list) -> None:
    logger.info(f'start run scan {keyword} {os} {region}')
    try:
        google_client = Google(proxy_manager.get_proxy_by_region(region))
        result, msg = await google_client.go(keyword, 3, os_map.get(os, None))
        if result:
            result_msg = (f'*{to_escape_string(keyword)}* \nregion:{region} os:{os_name_map.get(os, os)}\n'
                          f'_搜索结果_ \n')
            index = 0
            for k, v in result.items():
                domain = v.get('domain')
                if not domain:
                    continue
                index += 1
                result_msg += f'[{index}号]({to_escape_string(k)})\n'
                result_msg += f'>domain:{to_escape_string(v["domain"])}\n'
                result_list.append({
                    'keyword': keyword,
                    'os': os_name_map.get(os, os),
                    'region': region,
                    'domain': domain,
                    'create_at': datetime.now().strftime('%m-%d %H:%M:%S')
                })
            logger.info(f'found ad {index} from {keyword} {os} {region}')
            for chat_id in chat_ids:
                await send_message_to_bot(chat_id, result_msg, parse_mode='MarkdownV2')
        else:
            logger.info(f'not found ad {keyword} {os} {region}')
    except Exception as e:
        logger.error(f'run {keyword} {os} {region} fail {e}')


async def do_scan() -> None:
    """Send the alarm message."""
    keyword_list = timer_task_storage.get_value('keywords', [])
    sem = timer_task_storage.get_value('sem', 5)
    logger.info(f'start run scan {keyword_list}')
    chat_ids = timer_task_storage.get_value('chat_ids', [])
    if (not keyword_list) or (not chat_ids):
        logger.info(f'scan task not keyword or chat_ids')
        return
    os_list = [2, 4]
    region_list = list(proxy_manager.proxy_map.keys())
    task_gen = itertools.product(keyword_list, os_list, region_list)
    result = []
    task_manager = AsyncTaskManager(sem)
    for keyword, os, region in task_gen:
        await task_manager.add_task(scan_one, keyword=keyword, os=os, region=region,
                                    chat_ids=chat_ids, result_list=result)
    await task_manager.run()
    if result:
        now = datetime.now()
        now_ts = int(now.timestamp())
        filename = f'result_{now_ts}'
        json_manager.save_file(result, filename)
        history_list: list = history_html_storage.get_value('history', [])
        history_list.append({now.strftime('%Y-%m-%d %H:%M:%S'): filename})
        history_list = history_list[-50:]
        history_html_storage.set_value('history', history_list)
        text = f'访问以下网站查看结果\nhttps://tg.jiamid.com/{filename}'
        for chat_id in chat_ids:
            await send_message_to_bot(chat_id, text)
    logger.info('success to end scan task')
