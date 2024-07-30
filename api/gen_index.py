# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 15:19
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : gen_index.py
# @Software: PyCharm
from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from commonts.storage_manager import history_html_storage

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def gen_index():
    return generate_index_html()


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
        for date_str, result_id in item.items():
            table_html += "<tr>"
            table_html += f"<td>{date_str}</td>"
            table_html += f"<td><a href='/r/{result_id}'>{result_id}</a></td>"
            table_html += "</tr>"
    table_html += "</table></div>"
    return table_html


def generate_index_html():
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
    return full_html
