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
    快手 热榜
    """

    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://www.kuaishou.com/?isHome=1'
        self.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

    def crawls_parse(self):
        resp = self.crawls_getresponse()
        result_text_tmp = re.search(r'window.__APOLLO_STATE__=(.*);\(function\(\)', resp.text, re.IGNORECASE)
        result_json = json.loads(result_text_tmp.group(1)).get('defaultClient', {}) if result_text_tmp else {}
        result_list = []
        first_num = 0
        for each in result_json.get('$ROOT_QUERY.visionHotRank({"page":"home"})', {}).get('items', []):
            first_num += 1
            hot_dic = dict()
            hot_dic["title"] = result_json.get(each.get("id", ""), {}).get("name", "")
            hot_dic["desc"] = ""
            hot_dic["hot"] = result_json.get(each.get("id", ""), {}).get("hotValue", "")
            hot_dic["index"] = first_num
            try:
                post_tmp = result_json.get(each.get("id", ""), {}).get("poster", "")
                id_tmp = re.search(r'clientCacheKey=([A-Za-z0-9]+)', post_tmp).group(1)
            except:
                id_tmp = ""
            hot_dic["url"] = f"https://www.kuaishou.com/short-video/{id_tmp}" if id_tmp else ""
            hot_dic["mobileUrl"] = f"https://www.kuaishou.com/short-video/{id_tmp}" if id_tmp else ""

            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list


if __name__ == '__main__':
    info = Crawls().crawls_run()
    print(info)
