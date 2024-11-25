# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 15:29
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : util.py
# @Software: PyCharm
from fastapi import Request
from commonts.storage_manager import iptable_storage
from loguru import logger

def is_white_ip(req:Request):
    user_ip = req.headers.get('x-real_ip')
    logger.info(f'user_ip:{user_ip}')
    white_ip = iptable_storage.get_value('white',[])
    if user_ip in white_ip:
        return True
    return False



def to_escape_string(string):
    string = str(string)
    return string.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]").replace("(",
                                                                                                          "\\(").replace(
        ")", "\\)").replace("~", "\\~").replace("`", "\\`").replace(">", "\\>").replace("#", "\\#").replace("+",
                                                                                                            "\\+").replace(
        "-", "\\-").replace("=", "\\=").replace("|", "\\|").replace("{", "\\{").replace("}", "\\}").replace(".",
                                                                                                            "\\.").replace(
        "!", "\\!")
