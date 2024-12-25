# -*- coding: utf-8 -*-
# @Time    : 2024/1/11 15:59
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : search.py
# @Software: PyCharm
import aiohttp
from loguru import logger
from urllib.parse import urlparse
from lxml import etree
import random


class Google:
    useragent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
    ]

    def __init__(self, proxy=None):
        self.proxy = None
        self.proxy_auth = None

        if proxy:
            # Proxy
            if proxy.startswith('http'):
                proxy = proxy.replace('https://', 'http://')
            else:
                proxy = 'http://' + proxy

            self.proxy = proxy
            if self.proxy:
                split_list = self.proxy.split(':')
                if len(split_list) == 5:
                    self.proxy = f'http:{split_list[1]}:{split_list[2]}'
                    username = split_list[3]
                    password = split_list[4]
                    self.proxy_auth = aiohttp.BasicAuth(username, password, encoding='utf-8')

    def get_useragent(self):
        return random.choice(self.useragent_list)

    async def request(self, method: str, url: str, **kwargs):
        timeout = aiohttp.ClientTimeout(total=10)
        conn = aiohttp.TCPConnector(verify_ssl=False, limit_per_host=1)
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            async with session.request(method=method, url=url, **kwargs) as resp:
                html = await resp.text()
                return html

    async def search(self, keyword, results, lang, start, ua=None):
        headers = {
            "User-Agent": ua if ua else self.get_useragent()
        }
        params = {
            "q": keyword,
            "hl": lang,
            "start": start,
            "num": results + 2
        }
        api = f'https://www.google.com/search?' + '&'.join([f'{k}={v}' for k, v in params.items()])
        html = await self.request('GET', api,
                                  proxy=self.proxy,
                                  proxy_auth=self.proxy_auth,
                                  headers=headers,
                                  )
        return html

    async def old_go(self, keyword, page=1, ua=None):
        ad_map = {}
        start = 0
        msg = ''
        error = ''
        page_size = 10
        while page > 0:
            try:
                html = await self.search(keyword, page_size, 'en', start, ua)
                dom = etree.HTML(html)
                ads_a = dom.xpath('//div[@role="region"]//a')
                for ad in ads_a:
                    pcu = ad.get('data-pcu', '')
                    href = ad.get('href', '')
                    rw = ad.get('data-rw')
                    if rw is not None:
                        ad_map[rw] = {'pcu': pcu, 'href': href}
                m_ads_a = dom.xpath('//div[@data-text-ad="1"]//a[@role="presentation"]')
                for ad in m_ads_a:
                    pcu = ad.get('data-pcu', '')
                    href = ad.get('href', '')
                    rw = ad.get('data-rw')
                    if rw is not None:
                        ad_map[rw] = {'pcu': pcu, 'href': href}
            except Exception as e:
                error += f'\npage {page} error:{str(e)}'
                logger.error(e)
            page -= 1
            start += page_size
        msg += error
        clear_ad_map = {}
        domains = []
        for k, v in ad_map.items():
            href = v.get('href', '')
            domain = urlparse(href).netloc
            if domain not in domains:
                domains.append(domain)
                v['domain'] = domain
                clear_ad_map[k] = v
        return clear_ad_map, msg

    async def go(self, keyword, page=1, ua=None):
        ad_map = {}
        start = 0
        msg = ''
        error = ''
        page_size = 10
        while page > 0:
            try:
                html = await self.search(keyword, page_size, 'en', start, ua)
                dom = etree.HTML(html)
                ads_a = dom.xpath('//div[@role="region"]//a')
                for ad in ads_a:
                    # pcu = ad.get('data-pcu', '')
                    href = ad.get('href', '')
                    rw = ad.get('data-rw')
                    if rw:
                        ad_map[rw] = {'rw': rw, 'href': href}
                m_ads_a = dom.xpath('//div[@data-text-ad="1"]//a[@role="presentation"]')
                for ad in m_ads_a:
                    # pcu = ad.get('data-pcu', '')
                    href = ad.get('href', '')
                    rw = ad.get('data-rw')
                    if rw:
                        ad_map[rw] = {'rw': rw, 'href': href}
            except Exception as e:
                error += f'\npage {page} error:{str(e)}'
                logger.error(e)
            page -= 1
            start += page_size
        msg += error
        clear_ad_map = {}
        for k, v in ad_map.items():
            href = v.get('href', '')
            domain = urlparse(href).netloc
            v['domain'] = domain
            clear_ad_map[domain] = v
        return clear_ad_map, msg
