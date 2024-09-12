# -*- coding: utf-8 -*-
# @Time    : 2024/1/11 15:59
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : search.py
# @Software: PyCharm
import json
import aiohttp
from loguru import logger
import time
from typing import List, Dict
from anyio import Path
import base64
from lxml import etree
import random
import re
# from curl_cffi import requests
import requests
# from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright, Playwright, Page, BrowserContext
from typing import Callable


class AsyncTaskManager:
    """
    异步任务管理
    task_manager = AsyncTaskManager(self.sem_num)
    await task_manager.add_task(new_task, params=params)
    await task_manager.run()
    asyncio.run(m.run())
    """
    tasks = []

    def __init__(self, max_sem: int):
        self.sem = asyncio.Semaphore(max_sem)

    async def run_with_sem(self, task: Callable, **kwargs):
        async with self.sem:
            await task(**kwargs)

    async def add_task(self, task: Callable, **kwargs):
        new_task = asyncio.create_task(self.run_with_sem(task, **kwargs))
        self.tasks.append(new_task)

    async def run(self):
        tasks = self.tasks[:]
        self.tasks = []
        await asyncio.gather(*tasks)


def add_params_str(params_str, url):
    # 查找 URL 中是否有 adurl 参数
    c = re.search(r'[?&]adurl=', url)
    if c:
        # 在 adurl 参数之前插入新的查询参数
        return url[:c.start() + 1] + params_str + "&" + url[c.start() + 1:]
    else:
        # 如果没有 adurl 参数，根据 URL 中是否有查询参数来添加合适的分隔符
        return url + ('?' if '?' not in url else '&') + params_str


def check_nis(url, nis):
    nis = str(nis)
    # 查找 URL 中是否有 nis 参数
    c = re.findall(r'[?&]nis=([^&]*)', url)
    if c and c[0] == nis:
        return url  # 如果 nis 的值等于 b，返回原始 URL
    elif c:
        # 替换 URL 中的 nis 参数值为新的值
        return re.sub(r'([?&])nis=([^&]*)', r'\1nis=' + nis, url)
    else:
        # 如果没有 nis 参数，则添加它
        return add_params_str(f'nis={nis}', url)


def detail_a(a):
    attributionsourceid = a.get('attributionsourceid')
    attributiondestination = a.get('attributiondestination')
    if attributionsourceid and attributiondestination:
        n = 2
    else:
        attributionsrc = a.get('attributionsrc')
        if attributionsrc != None:
            n = 6
        else:
            n = 7

    if a.get('agdh') == 'fvd3vc':
        rw = a.get('rw')
        vid = a.get('ved')
        url = f'{rw}&ved={vid}'
    else:
        url = a.get('href')

    url = check_nis(url, n)
    return url


class Google:
    useragent_list = [
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    ]

    def __init__(self, proxy=None):
        self.proxies = None
        self.proxy = None
        self.proxy_auth = None
        self.proxy_cffi_auth = None

        if proxy:
            # Proxy
            if proxy.startswith('http'):
                proxy = proxy.replace('https://', 'http://')
            else:
                proxy = 'http://' + proxy
            self.proxies = {
                'http': proxy
            }
            self.proxy = proxy
        if self.proxy:
            split_list = self.proxy.split(':')
            if len(split_list) == 5:
                self.proxy = f'http:{split_list[1]}:{split_list[2]}'
                username = split_list[3]
                password = split_list[4]
                self.proxy_cffi_auth = (username, password)
                self.proxy_auth = aiohttp.BasicAuth(username, password, encoding='utf-8')

    def get_useragent(self):
        return random.choice(self.useragent_list)

    async def request(self, method: str, url: str, **kwargs):
        timeout = aiohttp.ClientTimeout(total=10)
        conn = aiohttp.TCPConnector(ssl=False, limit_per_host=5)
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            async with session.request(method=method, url=url, **kwargs) as resp:
                html = await resp.text()
                return html

    def sync_request(self, method: str, url: str, **kwargs):
        sess = requests.Session()
        resp = sess.request(method,
                            url,
                            timeout=10,
                            proxies=self.proxies,
                            **kwargs)
        print(resp.status_code)
        return resp.text

    async def start_search(self, keyword, results, lang, start, ua=None):
        html = await self.request('GET', "https://www.google.com/search",
                                  params={
                                      "q": keyword,
                                      "num": results,  # Prevents multiple requests
                                      "hl": lang,
                                      "start": start,
                                  },
                                  proxy=self.proxy,
                                  proxy_auth=self.proxy_auth,
                                  headers={
                                      "User-Agent": ua if ua else self.get_useragent()
                                  },
                                  )
        return html

    async def next_search(self, url, ua=None):
        html = await self.request('GET', url,
                                  proxy=self.proxy,
                                  proxy_auth=self.proxy_auth,
                                  headers={
                                      "User-Agent": ua if ua else self.get_useragent()
                                  },
                                  )
        return html

    async def visit(self, url, ua=None):
        status = True
        try:
            resp = self.sync_request('GET', url,
                                     headers={
                                         "User-Agent": ua if ua else self.get_useragent()
                                     }, )
        except Exception as e:
            logger.info(e)
            status = False
        return status

    async def async_playwright_visit(self, url, ua):
        ua = ua if ua else self.get_useragent()
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(proxy={
                    'server': self.proxy,  # 代理服务器地址
                    'username': self.proxy_cffi_auth[0],  # 如果需要身份验证
                    'password': self.proxy_cffi_auth[1]  # 如果需要身份验证
                })
                page = await browser.new_page()

                async def handle_route(route, request):
                    headers = request.headers.copy()
                    headers['user-agent'] = ua
                    await route.continue_(headers=headers)

                await page.route("**/*", handle_route)
                await page.goto(url)
                print(await page.title())
                for i in range(5):
                    await page.evaluate(f'scrollTo(0, scrollY + {i * 20});')
                    await page.wait_for_timeout(200)
                await browser.close()
            return True
        except Exception as e:
            print(f'WebError:{e}')
            return False

    async def go(self, keyword, max_page=1, ua=None, target=None):
        ad_map = {}
        start = 0
        msg = ''
        error = ''
        is_first = True
        next_url = ''
        page = 1
        while page <= max_page:
            flag = False
            try:
                print(f'get page {page}')
                if is_first:
                    html = await self.start_search(keyword, 20, 'en', start, ua)
                else:
                    html = await self.next_search(next_url, ua)
                dom = etree.HTML(html)
                ads_a = dom.xpath('//div[@role="region"]//a')
                next_a = dom.xpath('//a[@id="pnnext"]/@href')
                if next_a:
                    next_url = 'https://www.google.com' + next_a[0]
                print(f'find ad {len(ads_a)}')
                for ad in ads_a:
                    pcu = ad.get('data-pcu', '')
                    agch = ad.get('data-agch', None)
                    agdh = ad.get('data-agdh', None)
                    if pcu:
                        print(f'AD:{pcu}')
                    if agdh is None and agch is None:
                        continue
                    attributionsourceid = ad.get('attributionsourceid', None)
                    attributiondestination = ad.get('attributiondestination', None)
                    attributionsrc = ad.get('attributionsrc', None)
                    data_impdclcc = ad.get('data-impdclcc', None)
                    ved = ad.get('data-ved', None)
                    rw = ad.get('data-rw')
                    href = ad.get('href', None)
                    if pcu and rw:
                        ad_map[str(rw)] = {'pcu': pcu, 'href': href, 'ved': ved,
                                           'data_impdclcc': data_impdclcc,
                                           'attributionsourceid': attributionsourceid,
                                           'attributiondestination': attributiondestination,
                                           'attributionsrc': attributionsrc,
                                           'agch': agch,
                                           'agdh': agdh,
                                           'rw': rw
                                           }
                    if target and ((target in href) or target in pcu):
                        flag = True
                        break
            except Exception as e:
                error += f'\npage {page} error:{str(e)}'
                logger.error(e)
            page += 1
            start += 20
            if flag:
                break
        msg += error
        return ad_map, msg

    def check_in_target(self, targets, a):
        pcu = a["pcu"]
        href = a["href"]
        for target in targets:
            if (target in pcu) or (target in href):
                return target
        return False

    async def attack_ad(self, v, ua):
        times = 3
        url = detail_a(v)
        print(f'*Visit:{url}')
        while times > 0:
            # status = await self.visit(url, ua)
            status = await self.async_playwright_visit(url, ua)
            if status:
                return True
            times -= 1
        return False

    async def consume_ad(self, keyword: str, targets: List[str], run_mode=1, ua=None, detail_data=None, max_page=3):
        if detail_data is None:
            detail_data = {}
        if len(targets) == 1:
            find_target = targets[0]
        else:
            find_target = None
        result, msg = await self.go(keyword, max_page, ua, find_target)
        # logger.info(result)
        for k, v in result.items():
            attack_status = False
            in_target = self.check_in_target(targets, v)
            if run_mode and in_target:
                attack_status = await self.attack_ad(v, ua)
            if (not run_mode) and (not in_target):
                attack_status = await self.attack_ad(v, ua)
            if attack_status:
                if run_mode:
                    detail_data[in_target] = detail_data.get(in_target, 0) + 1
                else:
                    href = v["href"]
                    detail_data[href] = detail_data.get(href, 0) + 1


async def test():
    proxy_map = {
        "TW": "https://143.198.223.224:10000:JSQRpNv--region-TW-:PCCnxXI",
        "MM": "https://143.198.223.224:10000:JSQRpNv--region-MM-:PCCnxXI",
        "KH": "https://143.198.223.224:10000:JSQRpNv--region-KH-:PCCnxXI",
        "HK": "https://143.198.223.224:10000:JSQRpNv--region-HK-:PCCnxXI",
        "SG": "https://143.198.223.224:10000:JSQRpNv--region-SG-:PCCnxXI",
        "PH": "https://143.198.223.224:10000:JSQRpNv--region-PH-:PCCnxXI",
        "MY": "https://143.198.223.224:10000:JSQRpNv--region-MY-:PCCnxXI"
    }
    detail_data = {}
    for k, v in proxy_map.items():
        bot = Google(v)
        await bot.consume_ad('阿里云国际站', targets=[
            'yovacloud',
            'littlepig.tech'
        ], detail_data=detail_data, max_page=1)
        print(detail_data)
    print(detail_data)


async def test2():
    proxy_map = {
        "TW": "https://143.198.223.224:10000:JSQRpNv--region-TW-:PCCnxXI",
        "MM": "https://143.198.223.224:10000:JSQRpNv--region-MM-:PCCnxXI",
        "KH": "https://143.198.223.224:10000:JSQRpNv--region-KH-:PCCnxXI",
        "HK": "https://143.198.223.224:10000:JSQRpNv--region-HK-:PCCnxXI",
        "SG": "https://143.198.223.224:10000:JSQRpNv--region-SG-:PCCnxXI",
        "PH": "https://143.198.223.224:10000:JSQRpNv--region-PH-:PCCnxXI",
        "MY": "https://143.198.223.224:10000:JSQRpNv--region-MY-:PCCnxXI"
    }
    detail_data = {}
    # bot = Google(proxy_map['HK'])
    """
代理主机: 206.189.39.47
端口号: 10000
用户名: JSQRpNv-76B12H-region-PH-session-QLX469-keeptime-5
密码: PCCnxXI
PROXY: 206.189.39.47:10000:JSQRpNv-76B12H-region-PH-session-QLX469-keeptime-5:PCCnxXI
    """
    """
HOST:  as.s2ncd4av.lunaproxy.net
PORT:  12233
USER:  user-lu2549090-region-ph
PASS:  Sam12345
PROXY: as.s2ncd4av.lunaproxy.net:12233:user-lu2549090-region-ph:Sam12345
    """

    async def run_bot(detail_data):
        # bot = Google('https://143.198.223.224:10000:JSQRpNv--region-SG-:PCCnxXI')
        # bot = Google('as.s2ncd4av.lunaproxy.net:12233:user-lu2549090-region-ph:Sam12345')
        bot = Google('https://143.198.223.224:10000:JSQRpNv--region-HK-:PCCnxXI')
        # bot = Google('206.189.39.47:10000:JSQRpNv-76B12H-region-PH-session-QLX469-keeptime-5:PCCnxXI')
        while detail_data.get('success_num', 0) < 1000:
            await bot.consume_ad('亚马逊云代理', ['yovacloud'], detail_data=detail_data, max_page=2)
            # await bot.consume_ad('亚马逊云代理商', [
            #     'yovacloud',
            #     'littlepig.tech'
            # ], detail_data=detail_data, max_page=2)
            print(detail_data)

    sem = 4
    task_manager = AsyncTaskManager(4)
    detail_data = {}
    for _ in range(sem):
        await task_manager.add_task(run_bot, detail_data=detail_data)
    await task_manager.run()
    print(detail_data)


if __name__ == '__main__':
    import asyncio

    asyncio.run(test2())
    # bot = Google('as.s2ncd4av.lunaproxy.net:12233:user-lu2549090-region-ph:Sam12345')
    # url = 'https://www.google.com/aclk?sa=l&ai=DChcSEwjA29eRx7WIAxXdEnsHHZWQAHQYABABGgJ0bQ&co=1&ase=2&gclid=EAIaIQobChMIwNvXkce1iAMV3RJ7Bx2VkAB0EAMYASAAEgI4h_D_BwE&sig=AOD64_3tOA1vrxlgfLmqkkvBf_tEj7heVA&q&nis=6&adurl&ved=2ahUKEwiKv9ORx7WIAxW7lK8BHT9nBTkQ0Qx6BAgEEAE'
    # bot.sync_request('GET', url,
    #                  headers={
    #                      "User-Agent": bot.get_useragent(),
    #                      # 'Host': 'www.xiaohuyun.com.cn'
    #                  }, data={})
