#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import time
import os

# 根目录
base_path = os.path.dirname(os.path.dirname(__file__))
"""
-------------------------ngo--------------------------
"""
DB_NAME = 'ApacheLog'
MONGO_URL = 'mongodb://localhost:27017/'

"""
------------------------------ 日志配置 ---------------------------------
"""
# 打印错误日志路径
LOG_PATH = "{}/media/error_log/{}.log".format(base_path, time.strftime("%Y%m%d"))
# 日志格式
logging.basicConfig(filename=LOG_PATH,
                    level=logging.INFO,
                    filemode='w',
                    format='%(asctime)s -- %(levelname)s -- [%(filename)s:%(lineno)d] -- %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S')

"""
------------------------------ 正则 ---------------------------------
"""
APACHE_LOG_RE = r'(?P<ip>.*?) - - \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>.*?) (?P<bytes>.*?)'
# APACHE_LOG_RE = r'(?P<ip>.*?) - - \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>.*?) (?P<bytes>.*?) (?P<referer>.*?) (?P<ua>.*?)'


"""
------------------------------ 文件后缀 ---------------------------------
"""
# 文章后缀
ARTICLE_EX = ["html", "htm"]
# 媒体后缀
MEDIA_EX = ["mpg"]
# 需要过滤的文件
FILTER_EX = ["css", "js"]

"""
------------------------------ 表头 ---------------------------------
"""
# 文章报表表头
ARTICLE_HEADER_LIST = ["URL", "文章标题", "访问人次", "访问IP数"]
# ip报表表头
IP_HEADER_LIST = ["IP", "访问次数", "访问文章数"]
# 完整报表表头
COMPLETE_HEADER_LIST = ["IP", "URL", "访问次数"]

"""
------------------------------ 路径 ---------------------------------
"""
# 表格路径
ARTICLE_FORMAT_PATH = "{}{}".format(base_path, "/media/analysis_rst/article_markdown.md")
IP_FORMAT_PATH = "{}{}".format(base_path, "/media/analysis_rst/ip_markdown.md")
COMPLETE_FORMAT_PATH = "{}{}".format(base_path, "/media/analysis_rst/final_markdown.md")
# log日志路径
APACHE_LOG_PATH = "{}{}".format(base_path, "/media/apache_log")

ARTICLE_FORMAT = 1
IP_FORMAT = 2
COMPLETE_FORMAT = 3
