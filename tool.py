import json
import random
import time

import requests
import pymysql
import redis
from hashlib import md5
from datetime import timedelta, datetime

from config import proxies
from config import MYSQL_DB
from config import REDIS_DB

# 接口返回的基础
Base_Back_Result = {
    "status": 200,  # 状态码
    "err_msg": "",  # 错误信息
    "res_inf": "",  # 各种类型
}
# 爬虫的基础类
class Crawler_Base:
    """
    热榜爬虫基础类
    """
    def __init__(self):
        self.index_url = ""
        self.timeout = 5
        self.headers = {
            'User-Agent': UserAgent_Base().random()
        }
        self.cookies = {}
        self.proxy_support = None
        self.proxy = get_proxy() if self.proxy_support else {}
        self.data = {}

    # 请求函数 默认get 有其他可以重写
    def crawls_getresponse(self):
        res = requests.get(url=self.index_url, headers=self.headers, proxies=self.proxy, data=self.data,
                           timeout=self.timeout, cookies=self.cookies)
        return res

    # 解析
    def crawls_parse(self):
        pass

    # 最终统一调用的函数
    def crawls_run(self):
        return self.crawls_parse()


# 关于 User_Agent_Pc
class UserAgent_Base:

    def __init__(self):
        self.ua = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.39",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.55",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.46",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.46",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.41",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.86",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
        "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    ]

    def random(self):
        return random.choice(self.ua)


# 获得代理函数
def get_proxy():
    return proxies


# Md5 加密函数 32 返回32位的加密结果
def md5_use(text: str) -> str:
    result = md5(bytes(text, encoding="utf-8")).hexdigest()
    # print(result)
    return result


# 获取md5之后的每个字符并计算ASCII码总和
def md5_ascii_sum(input_string):
    # 计算MD5值
    md5_hash = md5(input_string.encode()).hexdigest()

    # 遍历MD5的每个字符并计算ASCII码总和
    ascii_sum = sum(ord(char) for char in md5_hash)

    return ascii_sum


# 获取时间函数
def get_x_hours_ago(hours, rformat="%Y-%m-%d %H:%M:%S"):
    now = datetime.now()
    seven_hours_ago = now - timedelta(hours=hours)
    return seven_hours_ago.strftime(rformat)


# 数据库基本操作
def mysql_normal(sql='', method='do', db="mysql", sql_list=None):  # 测试版本 注意注释的问题
    """
    :param sql  需要执行的sql语句
    :param method   返回的方法 是只执行还是
    :param db  连接的数据库的库名
    :param sql_list 需要执行的语句值 tuple
    :return DO 成功执行返回1 错误返回0
            BACKALL 成功执行 返回数据 错误返回空
            BACKONE 成功执行 返回数据 错误返回空
    """
    if sql_list is None:
        sql_list = []
    conn = pymysql.connect(host=MYSQL_DB["host"], port=MYSQL_DB["port"], user=MYSQL_DB["user"],
                           passwd=MYSQL_DB["passwd"], db=str(db),
                           charset='utf8mb4')
    cursor = conn.cursor()
    if method == "fetchall":
        try:
            cursor.execute(sql, sql_list)
            conn.commit()
            fetchall = cursor.fetchall()
            cursor.close()
            conn.close()
            return fetchall
        except Exception as e:
            print(e)
            cursor.close()
            conn.close()
            return ()
    elif method == "fetchone":
        try:
            cursor.execute(sql, sql_list)
            conn.commit()
            fetchall = cursor.fetchone()
            cursor.close()
            conn.close()
            return fetchall
        except Exception as e:
            print(e)
            cursor.close()
            conn.close()
            return ()
    elif method == "insert":
        try:
            cursor.execute(sql, sql_list)
            conn.commit()
            cursor.close()
            conn.close()
            return 1
        except Exception as e:
            print(e)
            cursor.close()
            conn.close()
            return 0
    elif method == "update" or method == "do":
        try:
            cursor.execute(sql, sql_list)
            conn.commit()
            cursor.close()
            conn.close()
            return 1
        except Exception as e:
            print(e)
            cursor.close()
            conn.close()
            return 0
    cursor.close()
    conn.close()


# 获取热点区间位次变化
def get_hot_title_ranking(title: str, board_type, hours: int = 24, rformat="%Y-%m-%d %H:%M:%S"):
    """
    :param title:
    :param board_type: 榜单的ID 必填
    :param hours: 默认24小时内
    :return:
    """
    xtime = get_x_hours_ago(hours=hours)
    # print(xtime)
    sql = "select index_num,get_time from {} where title=%s and get_time>%s and board_type=%s".format(MYSQL_DB["info_table_name"])
    fetchall = mysql_normal(sql,method="fetchall", db=MYSQL_DB["db"], sql_list=(
                                                            pymysql.converters.escape_string(title),
                                                            pymysql.converters.escape_string(xtime), board_type))
    # print(fetchall)
    result_lis = [[i[0], i[1].strftime(rformat)] for i in fetchall]
    # print(result_lis)
    return result_lis


def get_min_time(time_strings_lis: list, rformat="%Y-%m-%d %H:%M:%S"):  # 给一个时间列表 返回时间中最早的时间
    # 将字符串转换为datetime对象
    datetime_objects = [datetime.strptime(time_str, rformat) for time_str in time_strings_lis]

    # 对列表进行排序
    # sorted_times = sorted(datetime_objects)

    # 找到最早的时间
    earliest_time = min(datetime_objects)

    return earliest_time.strftime(rformat)


# 计算关键词搜索的结果 返回可以直接展示的内容
def count_search_result(result_lis, rformat="%Y-%m-%d %H:%M:%S", ):  # 计算搜索的结果 排序海鸥在榜时间
    lis_dic = {}

    for each in result_lis:
        each_md5 = md5_use(each[0]+str(each[2]))  # key 是用标题和榜单的类型进行拼接
        if each_md5 not in lis_dic:
            lis_dic[each_md5] = {
                "title": each[0],
                "index_num": each[1],
                "board_type": each[2],
                "get_time": each[3].strftime(rformat),
                "id": each[4],  # id是自增的，越大的越靠前
                "pc_url": each[5],
                "count": 10
            }
        else:  # 这里判断如果出现就进行比较
            if int(lis_dic[each_md5]["index_num"]) > int(each[1]):  # 如果排名大就替换
                lis_dic[each_md5]["index_num"] = each[1]
            elif lis_dic[each_md5]["id"] < each[4]:  # 如果获取时间 通过ID进行判断
                lis_dic[each_md5]["get_time"] = each[3].strftime(rformat)
            lis_dic[each_md5]["count"] += 10
    return list(lis_dic.values())


# 获取关键词搜索结果
def get_search_keywords(keywords: str, board_type=0, hours: int = 24, rformat="%Y-%m-%d %H:%M:%S"):
    """
    :param keywords:
    :param board_type: 榜单的ID 必填
    :param hours: 默认24小时内
    :return:
    """
    # print(time.time())
    xtime = get_x_hours_ago(hours=hours)
    if board_type:
    # print(xtime)
        sql = "select title,index_num,board_type,get_time,id,pc_url from {} where title like %s and get_time>%s and board_type=%s".format(MYSQL_DB["info_table_name"])
        fetchall = mysql_normal(sql, method="fetchall", db=MYSQL_DB["db"], sql_list=(
                                                            pymysql.converters.escape_string('%'+keywords+'%'),
                                                            pymysql.converters.escape_string(xtime),
                                                            board_type))

    else:
        sql = "select title,index_num,board_type,get_time,id,pc_url from {} where title like %s and get_time>%s".format(MYSQL_DB["info_table_name"])
        fetchall = mysql_normal(sql,method="fetchall", db=MYSQL_DB["db"], sql_list=(
                                                            pymysql.converters.escape_string('%'+keywords+'%'),
                                                            pymysql.converters.escape_string(xtime)))
    # print(fetchall)
    return count_search_result(fetchall)


# redis 存储
def redis_normal(db="0", decode_responses=True):

    con = redis.Redis(host=REDIS_DB["host"], port=REDIS_DB["port"], decode_responses=decode_responses, db=db, password=REDIS_DB["passwd"])

    return con


# 获取单独某个key下的某个键值
def redis_noremal_gethk_get(board_type, task_keyname="board_title", db=REDIS_DB["db"]):
    """
    :param board_type: 榜单的ID
    :param task_keyname: 榜单里的key
    :param db: 默认0
    :return:
    """
    con = redis_normal(db=db)
    key_name = con.hget(board_type, task_keyname)
    con.close()
    return key_name


# 获取单独某个key下的某个键值
def redis_noremal_string_get(task_keyname="board_title", db=REDIS_DB["db"]):
    """
    :param task_keyname: 需要取值的key
    :param db: 默认0
    :return:
    """
    con = redis_normal(db=db)
    key_result = con.get(task_keyname)
    con.close()
    return key_result


# 获取单独某个key下的某个键值
def redis_noremal_hash(type_, keyname="", filed="", db=REDIS_DB["db"], amount=1):
    """
    :param board_type: 榜单的ID
    :param task_keyname: 榜单里的key
    :param db: 默认0
    :return:
    """
    con = redis_normal(db=db)
    if type_ == "hget":  #  获取某个key下的某个键值
        info = con.hget(keyname, filed)
        con.close()
    if type_ == "hgetall":  #  获取某个key下的所有键值
        info = con.hgetall(keyname)
        con.close()
    if type_ == "hincrby":  # 增加某个字段的值
        info = con.hincrby(keyname, filed, amount)
        con.close()
    if type_ == "hexists":  # 是否存在某个字段
        info = con.hexists(keyname, filed)
        con.close()

    con.close()
    return info


# redis 获取当前redis里热榜信息，通过平台表获取
def redis_normal_get_now_db(db=REDIS_DB["db"], board_type_list: list = None, decode_responses=True):
    """
    :param db: 默认db0
    :param board_type_list: 传递
    :param decode_responses: 默认转
    :return: [{},{}]
    """

    con = redis_normal(db=db)
    result_lis = []
    if board_type_list:
        for board_type in board_type_list:
            board_dic = {}
            board_inf = con.hgetall(str(board_type))
            board_dic["board_type"] = board_type
            board_inf["result"] = json.loads(board_inf["result"])
            board_dic["board_info"] = board_inf
            if board_inf:  # 可能会有没有的平台
                result_lis.append(board_dic)
    else:
        sql = "select board_type from {} where board_status=1".format(MYSQL_DB["platform_table_name"])
        board_type_list = [each[0] for each in mysql_normal(sql,method="fetchall",db=MYSQL_DB["db"])]
        # print(board_type_list)
        # print(con.hgetall("2"))
        for board_type in board_type_list:
            board_dic = {}
            board_inf = con.hgetall(str(board_type))
            board_dic["board_type"] = board_type
            board_inf["result"] = json.loads(board_inf["result"])
            board_dic["board_info"] = board_inf
            if board_inf:  # 可能会有没有的平台
                result_lis.append(board_dic)

    con.close()
    return result_lis


##### 小宇宙
def get_comment_xiaoyuzhou(eid, loadMoreKey=""):

    headers = {
        'Host': 'car-tesla-api-beta.xiaoyuzhoufm.com',
        'Cookie': '[object Undefined]',
        'x-jike-client-type': 'xyz-weapp',
        'accept': 'application/json, text/plain, */*',
        'xweb_xhr': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.5(0x13080510)XWEB/1100',
        # 'x-jike-device-id': '726ADEF0-B3BC-4875-89BB-2FFB132FDA85',
        'content-type': 'application/json',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wx4934a02480acb3d9/2/page-frame.html',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    json_data = {
        # 'eid': '658ae28eb8fd2bc06012d7f0',
        # 'eid': '65421f9267c3b425f574e977',
        'size': 1000, # 可以设置很大
        # 'loadMoreKey': {
        #     'direction': 'NEXT',
        #     'hotSortScore': 0.9512744540953,
        #     'id': '65a0e7f1152b01025ae0e1ec',
        # },
    }
    if eid:
        json_data['eid'] = eid
    if loadMoreKey:
        json_data['loadMoreKey'] = loadMoreKey

    response = requests.post(
        'https://car-tesla-api-beta.xiaoyuzhoufm.com/1.0/comment/list-primary-by-hot',
        headers=headers,
        json=json_data,
        timeout=5
    )

    # print(response.text)
    return response


if __name__ == "__main__":
    print(md5_use("沥心沙"))  # b7d672aeeb30c45918420d90a22f5195
    print(md5_ascii_sum("沥心沙"))  # b7d672aeeb30c45918420d90a22f5195
    exit()
    info = get_search_keywords("换贾玲背张小斐",hours=640)
    print(info)
    print(time.time())
    exit()
    get_comment_xiaoyuzhou("658ae28eb8fd2bc06012d7f0")
    exit()

    print(redis_noremal_gethk_get(board_type=1, task_keyname="board_title"))
    exit()

    # get_hot_title_ranking("冬天就在雪地里相爱", board_type=19, hours=3)
    # exit()

    # time_ = get_x_hours_ago(5)
    # print(time_)
    # exit()

    # result_lis = redis_normal_get_now_db()
    # print(result_lis)
    # exit()

    # UserAgent = UserAgent_Base().random()
    # print(get_proxy())
