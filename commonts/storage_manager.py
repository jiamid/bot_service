# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 15:27
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : storage_manager.py
# @Software: PyCharm
import json
import base64
from loguru import logger
import os


class StorageManager:

    def __init__(self, filename: str, default_data: dict, dir_path: str = 'b64_db'):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.file_path = f'{dir_path}/{filename}.b64'
        self.data: dict = self.read_file()
        if not self.data:
            self.data = default_data
            self.save_file()

    def get_value(self, key, default):
        return self.data.get(key, default)

    def del_key(self, key):
        del self.data[key]
        self.save_file()

    def set_value(self, key, value):
        self.data[key] = value
        self.save_file()

    def add_to_key(self, key, value):
        key_list = self.data.get(key, [])
        if value not in key_list:
            key_list.append(value)
        self.set_value(key, key_list)
        logger.info(f'add {value} {key}:{key_list}')

    def del_from_key(self, key, value):
        key_list = self.data.get(key, [])
        if value in key_list:
            key_list.remove(value)
        self.set_value(key, key_list)
        logger.info(f'del {value} {key}:{key_list}')

    def save_file(self):
        try:
            # 将 JSON 数据转为字符串
            json_str = json.dumps(self.data)
            # 将字符串进行 base64 编码
            encoded_data = base64.b64encode(json_str.encode()).decode()
            # 写入文件
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(encoded_data)
        except Exception as e:
            print(e)
            logger.error('save_file error')

    def read_file(self):
        if not os.path.exists(self.file_path):
            return {}
        # 从文件读取 base64 编码的数据
        with open(self.file_path, 'r', encoding='utf-8') as file:
            encoded_data = file.read()
        # 进行 base64 解码
        decoded_data = base64.b64decode(encoded_data.encode()).decode()
        # 将解码后的字符串转回 JSON
        json_data = json.loads(decoded_data)
        return json_data


timer_task_storage = StorageManager('timer_task', {
    'keywords': [
        '国际阿里云',
        # '阿里云',
        # '阿里云代理商',
        # '国际阿里云代理商',
        # '匿名阿里云',
        # '阿里云服务器',
        # '免实名阿里云服务器',
        # '阿里云开户',
        # '阿里云实名账号',
        # '阿里云账号',
        # '国际腾讯云',
        # '腾讯云',
        # '腾讯云代理商',
        # '国际腾讯云代理商',
        # '匿名腾讯云',
        # '免实名腾讯云服务器',
        # '腾讯云服务器',
        # '腾讯云开户',
        # '腾讯云实名账号',
        # '腾讯云账号',
        # '华为云',
        # '国际华为云',
        # '华为云代理',
        # '亚马逊云',
        # 'aws',
        # '亚马逊云服务器',
        # '亚马逊云开户',
        # '亚马逊云账号',
        # '亚马逊云代理商',
        # 'aws代理',
        # '谷歌云',
        # 'gcp',
        # '谷歌云代理商',
        # '谷歌云服务器',
        # '谷歌云开户',
        # '谷歌云账号',
        # 'gcp代理',
        # '微软云',
        # 'azure',
        # '微软云代理商',
        # '微软云服务器',
        # '微软云开户',
        # '微软云账号',
        # '阿里云国际站',
        # '腾讯云国际站'
    ],
    'targets': [],
    'chat_ids': [],
    'sem': 5
})

proxys_storage = StorageManager('proxy_map', {
    'MM': 'https://143.198.223.224:10000:JSQRpNv--region-MM-:PCCnxXI',
    'KH': 'https://143.198.223.224:10000:JSQRpNv--region-KH-:PCCnxXI',
    'HK': 'https://143.198.223.224:10000:JSQRpNv--region-HK-:PCCnxXI',
    'SG': 'https://143.198.223.224:10000:JSQRpNv--region-SG-:PCCnxXI',
    'PH': 'https://143.198.223.224:10000:JSQRpNv--region-PH-:PCCnxXI',
    'MY': 'https://143.198.223.224:10000:JSQRpNv--region-MY-:PCCnxXI',
})

history_html_storage = StorageManager('history_html', {
    'history': []
})

group_storage = StorageManager('group', {

})


class ProxyManager:
    proxy_map = proxys_storage.data

    def refresh_proxy(self):
        self.proxy_map = proxys_storage.data

    def get_keys_str(self):
        keys = self.proxy_map.keys()
        return ' '.join(keys)

    def get_proxy_by_region(self, region):
        return self.proxy_map.get(region, None)


proxy_manager = ProxyManager()

iptable_storage = StorageManager('iptable', {
    'white': []
})
