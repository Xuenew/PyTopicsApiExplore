# -*- coding: utf-8 -*-

"""
@author: otll
@time: 2023/11/11
"""
import time

from tool import Crawler_Base


class Crawls(Crawler_Base):
    """
    澎湃热门
    """
    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar'

    def crawls_parse(self):
        result_list = []
        first_num = 0
        for each in self.crawls_getresponse().json().get('data', {}).get('hotNews', []):
            first_num += 1
            hot_dic = dict()
            hot_dic["h_id"] = each.get("contId", "")
            hot_dic["title"] = each.get("name", "")
            hot_dic["desc"] = ""
            hot_dic["index"] = first_num
            hot_dic["url"] = f"https://www.thepaper.cn/newsDetail_forward_{hot_dic['h_id']}" if hot_dic.get('h_id') else ""
            hot_dic["mobileUrl"] = f"https://m.thepaper.cn/newsDetail_forward_{hot_dic['h_id']}" if hot_dic.get('h_id') else ""

            result_list.append(hot_dic)
        return result_list


if __name__ == '__main__':
    info = Crawls().crawls_run()
    print(info)
