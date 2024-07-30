# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 15:29
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : util.py
# @Software: PyCharm
from loguru import logger
from datetime import datetime
from collections import defaultdict
from .storage_manager import history_html_storage
import os

dir_path = 'ad_html'
if not os.path.exists(dir_path):
    os.makedirs(dir_path)


def to_escape_string(string):
    string = str(string)
    return string.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]").replace("(",
                                                                                                          "\\(").replace(
        ")", "\\)").replace("~", "\\~").replace("`", "\\`").replace(">", "\\>").replace("#", "\\#").replace("+",
                                                                                                            "\\+").replace(
        "-", "\\-").replace("=", "\\=").replace("|", "\\|").replace("{", "\\{").replace("}", "\\}").replace(".",
                                                                                                            "\\.").replace(
        "!", "\\!")


def generate_div_table_v2(data, now_time):
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
    table_html += f"<caption>广告搜索结果  {now_time.strftime('%Y-%m-%d %H:%M:%S')} </caption>"
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


def generate_ad_html(data, filename='index.html'):
    # filename = 'index.html'
    global dir_path
    now = datetime.now()
    table_html = generate_div_table_v2(data, now)
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
    with open(f'{dir_path}/{filename}', 'w', encoding='utf-8') as file:
        file.write(full_html)
    logger.info(f'success write html:{filename}')
    history_list: list = history_html_storage.get_value('history', [])
    history_list.append({now.strftime('%Y-%m-%d %H:%M:%S'): filename})
    history_list = history_list[-50:]
    history_html_storage.set_value('history', history_list)


def generate_index_table():
    history_list: list = history_html_storage.get_value('history', [])
    data = history_list[:]
    data.reverse()
    table_html = """
    <div class="table_box">
        <table>
            <caption>历史记录</caption>
            <tr><th>时间</th><th>链接</th></tr>
    """
    for item in data:
        for date_str, filename in item.items():
            table_html += "<tr>"
            table_html += f"<td>{date_str}</td>"
            table_html += f"<td><a href='/{filename}'>{filename}</a></td>"
            table_html += "</tr>"
    table_html += "</table></div>"
    return table_html


def generate_index_html():
    global dir_path
    filename = 'index.html'
    now = datetime.now()
    style_html = """
    <style>
    body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(to bottom, #c4f6c6, #4CAF50);
        }
        table {
            width: 100%;
            border-collapse: collapse;
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

        tr:nth-child(odd) {
            background-color: #c4f6c6;
        }

        tr:nth-child(even) {
            background-color: #ffffff;
        }

        td {
            border: none;
            padding: 8px;
            text-align: center;
            font-weight: bold;
        }

        td > a {
            text-decoration: none;
        }

        td > a::before {
            content: '🔗';
            margin-right: 5px; /* Adjust space between icon and text */
        }

        th {
            border: none;
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
            max-width: 1000px;
            height: 85%;
            margin: 2px auto;
            border: 2px solid #4CAF50;
            padding: 0;
            background-color: #f8f9fa;
            overflow: auto;
            border-radius: .7rem;
        }
    </style>
    """
    table_html = generate_index_table()
    full_html = f"""
    <html lang="zh">
    <head>
    <meta charset="UTF-8">
    {style_html}
    <title>AD Panel</title>
    </head>
    <body>
    <div class="bold_text">刷新时间 {now.strftime('%Y-%m-%d %H:%M:%S')}</div>
    {table_html}
    </body>
    </html>
    """

    with open(f'{dir_path}/{filename}', 'w', encoding='utf-8') as file:
        file.write(full_html)
    logger.info(f'success write html:{filename}')
