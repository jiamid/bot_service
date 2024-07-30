# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 15:19
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : gen_ad_result.py
# @Software: PyCharm
from fastapi import APIRouter
from commonts.json_manager import json_manager
from datetime import datetime
from collections import defaultdict
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get('/r/{result_id}', response_class=HTMLResponse)
async def gen_ad_result(result_id: str):
    data = json_manager.read_file(result_id)
    return generate_ad_html(data)


def generate_div_table_v2(data):
    # 构建嵌套的 defaultdict 结构
    grouped_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    # 填充数据
    for item in data:
        keyword = item['keyword']
        os = item['os']
        region = item['region']
        domain = item['domain']
        create_at = item['create_at']
        grouped_data[keyword][os][region].append({'domain': domain, 'create_at': create_at})

    table_html = """<div class="table_box">
        <table>
        """
    table_html += f"<caption>广告搜索结果</caption>"
    table_html += '<tr><th>Keyword</th><th>OS</th><th>Region</th><th>Domains</th><th>Time</th></tr>'
    for keyword, os_dict in grouped_data.items():
        keyword_rowspan = sum(sum(len(domains) for domains in region_dict.values()) for region_dict in os_dict.values())
        keyword_first_row = True
        for os, region_dict in os_dict.items():
            os_rowspan = sum(len(domains) for domains in region_dict.values())
            os_first_row = True
            for region, domains in region_dict.items():
                region_rowspan = len(domains)
                region_first_row = True
                for domain_dict in domains:
                    domain = domain_dict['domain']
                    this_create_at = domain_dict['create_at']
                    table_html += '<tr>'
                    if keyword_first_row:
                        table_html += f'<td rowspan="{keyword_rowspan}">{keyword}</td>'
                        keyword_first_row = False

                    if os_first_row:
                        table_html += f'<td rowspan="{os_rowspan}">{os}</td>'
                        os_first_row = False

                    if region_first_row:
                        table_html += f'<td rowspan="{region_rowspan}">{region}</td>'
                        region_first_row = False

                    table_html += f'<td>{domain}</td><td>{this_create_at}</td>'
                    table_html += '</tr>'
        table_html += '<tr class="blank_tr"> <td colspan="5"></td></tr>'
    table_html += '</table></div>'
    return table_html


def generate_ad_html(data):
    now = datetime.now()
    table_html = generate_div_table_v2(data)
    style_html = """
    <style>
            body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            /*height: 100vh;*/
            margin: 0;
            background: linear-gradient(to bottom, #c4f6c6, #4CAF50);
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        .blank_tr {
            width: 100%;
            height: 50px;
            background-color: #4CAF50;
        }

        caption {
            padding: 8px;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }

        .bold_text {
            color: #4CAF50;
            font-weight: bold;
        }


        td {
            padding: 8px;
            text-align: center;
            font-weight: bold;
            border: 1px solid #4CAF50;
        }

        th {
            border: 1px solid #4CAF50;
            background-color: #4CAF50;
            color: white;
            position: sticky;
            text-align: center;
            padding: 8px;
            top: 0;
            z-index: 1;
        }

        .table_box {
            min-width: 800px;
            max-width: 1200px;
            margin: 2px auto;
            border: 2px solid #4CAF50;
            padding: 0;
            background-color: #f8f9fa;
            border-radius: .7rem;
        }
    </style>
    """
    full_html = f"""
    <html lang="zh">
    <head>
    <meta charset="UTF-8">
    {style_html}
    <title>Result {now.strftime('%Y-%m-%d %H:%M:%S')}</title>
    </head>
    <body>
    <div class="bold_text">{now.strftime('%Y-%m-%d %H:%M:%S')}</div>
    {table_html}
    </body>
    </html>
    """
    return full_html
