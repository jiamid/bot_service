# -*- coding: utf-8 -*-
# @Time    : 2023/12/20 11:44
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : doubao.py
# @Software: PyCharm
from loguru import logger
from volcengine.visual.VisualService import VisualService
from commonts.settings import settings


class DouBaoBot:
    def __init__(self):
        self.ak: str = settings.doubao_ak
        self.sk: str = settings.doubao_sk
        self.visual_service = VisualService()
        self.visual_service.set_ak(self.ak)
        self.visual_service.set_sk(self.sk)

    async def text_to_img(self, prompt):
        try:
            form = {
                "req_key": "high_aes_general_v14",
                "prompt": prompt,
                "model_version": "general_v1.4",
                "vida_enable_module": "score_total_ds",
                "return_url": True
            }
            img_url = ''
            tips = ''
            res_data = self.visual_service.high_aes_smart_drawing_v2(form)
            if res_data.get('code') == 10000:
                img_url = res_data.get('data', {}).get('image_urls', [''])[0]
                tips = res_data.get('data', {}).get('rephraser_result', '')
            return {
                'url': img_url,
                'tips': tips
            }
        except Exception as e:
            logger.error(e)
            return {}