# -*- coding: utf-8 -*-

"""
@author: otll
@time: 2023/11/11
"""
import json

import requests

from tool import Crawler_Base


class Crawls(Crawler_Base):
    """
    36氪 热榜
    """

    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://gateway.36kr.com/api/mis/nav/home/nav/rank/hot'

    def crawls_getresponse(self):
        data = {"partner_id": "wap",
                "param": {
                    "siteId": 1,
                    "platformId": 2
                }}
        self.headers.update({'Content-Type': 'application/json'})
        res = requests.post(url=self.index_url, headers=self.headers, proxies=self.proxy, data=json.dumps(data),
                            timeout=self.timeout, cookies=self.cookies)
        return res

    def crawls_parse(self):
        result_list = []
        first_num = 0
        for each in self.crawls_getresponse().json().get('data', {}).get('hotRankList', []):
            tmp_data = each.get('templateMaterial', {})
            first_num += 1
            hot_dic = dict()
            hot_dic["h_id"] = each.get("itemId", "")
            hot_dic["title"] = tmp_data.get("widgetTitle", "")
            hot_dic["desc"] = ""
            hot_dic["pic"] = tmp_data.get("widgetImage", "")
            hot_dic["owner"] = tmp_data.get("authorName", "")
            hot_dic["data"] = tmp_data
            hot_dic["hot"] = tmp_data.get("statRead", "")
            hot_dic["index"] = first_num
            hot_dic["url"] = f"https://www.36kr.com/p/{hot_dic['h_id']}" if hot_dic.get('h_id') else ""
            hot_dic["mobileUrl"] = f"https://www.36kr.com/p/{hot_dic['h_id']}" if hot_dic.get('h_id') else ""

            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list


if __name__ == '__main__':
    info = Crawls().crawls_run()
    print(info)
