# -*- coding: utf-8 -*-

"""
@author: otll
@time: 2023/11/11
"""
import json
import re

import requests

from tool import Crawler_Base


class Crawls(Crawler_Base):
    """
    稀土掘金 热榜
    """

    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://api.juejin.cn/content_api/v1/content/article_rank?category_id=1&type=hot'

    def crawls_parse(self):
        result_list = []
        first_num = 0
        for each in self.crawls_getresponse().json().get('data', []):
            tmp_data = each.get('content', {})
            tmp2_data = each.get('content_counter', {})
            first_num += 1
            hot_dic = dict()
            hot_dic["h_id"] = tmp_data.get("content_id", "")
            hot_dic["title"] = tmp_data.get("title", "")
            hot_dic["hot"] = tmp2_data.get("hot_rank", "")
            hot_dic["index"] = first_num
            hot_dic["url"] = f"https://juejin.cn/post/{hot_dic['h_id']}" if hot_dic.get('h_id') else ""
            hot_dic["mobileUrl"] = f"https://juejin.cn/post/{hot_dic['h_id']}" if hot_dic.get('h_id') else ""

            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list


if __name__ == '__main__':
    info = Crawls().crawls_run()
    print(info)
