#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/17 10:33
# @Author   : 冉勇
# @File     : spider.py
# @Software : PyCharm
# @Desc     : 抓取小红书图文
import pandas as pd
import requests
import time
from utils.log_util import logger
from bs4 import BeautifulSoup
from datetime import datetime

# 需要替换为实际的cookie
cookie = 'customerClientId=087431735812996; x-user-id-creator.xiaohongshu.com=62fc3f3d000000001200e239; gid=yYf4yyj0SiSyyYf4yyj0Y7vMdSUEAidAxfDvEDyDDSvyK9q8Kl40xK888y8q8JY8Y8K0dWyJ; abRequestId=f2c0bbc6553c3d50ccb8c387010e0ecd; xsecappid=xhs-pc-web; a1=19547b30a49ql29k5y90t8o9tf3yn6f06les7lchg30000328532; webId=101e492aa14658124dc963e78d7b74cd; webBuild=4.62.3; web_session=0400698ff6d4da564cc6fb7b123a4b9281db23; unread={%22ub%22:%2264a65d2f0000000023035e63%22%2C%22ue%22:%2264a65d2f0000000023035e63%22%2C%22uc%22:1}; websectiga=82e85efc5500b609ac1166aaf086ff8aa4261153a448ef0be5b17417e4512f28; sec_poison_id=7e055836-4c95-4eb6-895b-629a058c9d5d; loadts=1747408439446'

# 请求头配置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Cookie': cookie

}


def get_note_content(url):
    """
    获取笔记内容和话题标签
    
    Args:
        url: 笔记URL
    
    Returns:
        tuple: (笔记内容, 话题标签字符串)
    """
    try:
        # 发送HTTP请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 解析HTML
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取笔记内容
        desc_elem = soup.find(id='detail-desc')
        content = desc_elem.text.strip() if desc_elem else ''

        # 获取话题标签
        tag_items = soup.find_all('a', class_='tag')
        tags = []
        for tag in tag_items:
            tag_text = tag.text.strip()
            if tag_text.startswith('#'):
                tags.append(tag_text[0:])  # 去掉#号

        # 如果内容仅包含话题标签,则将内容置空
        if content and all(tag in content for tag in tags) and len(''.join(tags)) >= len(content) * 0.8:
            content = ''

        return content, ' '.join(tags)

    except Exception as e:
        logger.error(f"处理URL时出错: {url}, 错误信息: {str(e)}")
        return '', ''


def main():
    # 输入文件路径
    input_file = r"demo1.xlsx"
    # 输出文件路径
    output_file = f"结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    try:
        # 读取Excel文件
        logger.info(f"开始读取文件: {input_file}")
        df = pd.read_excel(input_file)

        # 检查是否存在URL列
        if df.empty or len(df.columns) == 0:
            raise ValueError("Excel文件为空或格式不正确")

        # 获取URL列
        url_column = df.iloc[:, 0]

        # 存储结果
        contents = []
        tags = []

        # 处理每个URL
        total = len(url_column)
        for idx, url in enumerate(url_column, 1):
            logger.info(f"正在处理第 {idx}/{total} 个URL: {url}")
            content, tag = get_note_content(url)
            contents.append(content)
            tags.append(tag)

            # 添加3秒延时
            if idx < total:  # 如果不是最后一个URL
                logger.info("等待3秒后继续...")
                time.sleep(3)

        # 添加新列
        df['笔记内容'] = contents
        df['话题标签'] = tags

        # 保存结果
        logger.info(f"正在保存结果到: {output_file}")
        df.to_excel(output_file, index=False)
        logger.info("处理完成!")

    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        raise


if __name__ == "__main__":
    main()
