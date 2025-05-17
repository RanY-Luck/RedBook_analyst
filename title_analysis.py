#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/17 10:33
# @Author   : 冉勇
# @File     : title_analysis.py
# @Software : PyCharm
# @Desc     : 分析标题
import pandas as pd
import jieba
import jieba.analyse
from utils.log_util import logger
from collections import Counter
from datetime import datetime


def extract_keywords(title):
    """
    从标题中提取关键词
    
    Args:
        title: 标题文本
        
    Returns:
        list: 关键词列表
    """
    # 使用jieba.analyse.extract_tags提取关键词
    # topK设置提取前5个关键词，allowPOS设置允许的词性
    keywords = jieba.analyse.extract_tags(
        title,
        topK=5,
        allowPOS=('n', 'vn', 'v', 'a')  # 允许名词、动名词、动词、形容词
    )
    return keywords


def analyze_titles(input_file):
    """
    分析标题并统计关键词
    
    Args:
        input_file: 输入文件路径
        
    Returns:
        tuple: (关键词计数器, 关键词-标题映射字典)
    """
    try:
        # 读取Excel文件
        logger.info(f"正在读取文件: {input_file}")
        df = pd.read_excel(input_file)

        # 检查是否存在"笔记标题"列
        if '笔记标题' not in df.columns:
            raise ValueError("Excel文件中未找到'笔记标题'列")

        # 初始化计数器和映射字典
        keyword_counter = Counter()
        keyword_titles = {}

        # 处理每个标题
        total = len(df)
        for idx, title in enumerate(df['笔记标题'], 1):
            logger.info(f"正在处理第 {idx}/{total} 个标题")

            # 跳过空标题
            if pd.isna(title):
                continue

            # 提取关键词
            keywords = extract_keywords(str(title))

            # 更新计数器
            keyword_counter.update(keywords)

            # 更新关键词-标题映射
            for keyword in keywords:
                if keyword not in keyword_titles:
                    keyword_titles[keyword] = []
                if title not in keyword_titles[keyword]:
                    keyword_titles[keyword].append(title)

        return keyword_counter, keyword_titles

    except Exception as e:
        logger.error(f"处理文件时出错: {str(e)}")
        raise


def save_results(keyword_counter, keyword_titles, output_file):
    """
    保存分析结果
    
    Args:
        keyword_counter: 关键词计数器
        keyword_titles: 关键词-标题映射字典
        output_file: 输出文件路径
    """
    try:
        logger.info(f"正在保存结果到: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("标题关键词统计结果\n")
            f.write("=" * 50 + "\n\n")

            # 按频次降序排列
            for keyword, count in keyword_counter.most_common():
                f.write(f"关键词: {keyword}\n")
                f.write(f"出现次数: {count}\n")
                f.write("相关标题:\n")
                for title in keyword_titles[keyword]:
                    f.write(f"  - {title}\n")
                f.write("\n")

        logger.info("保存完成!")

    except Exception as e:
        logger.error(f"保存结果时出错: {str(e)}")
        raise


def main():
    # 输入输出文件路径
    input_file = r"结果_20250517_142553.xlsx"
    output_file = f"标题分析_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    try:
        # 分析标题
        keyword_counter, keyword_titles = analyze_titles(input_file)

        # 保存结果
        save_results(keyword_counter, keyword_titles, output_file)

    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        raise


if __name__ == "__main__":
    main()
