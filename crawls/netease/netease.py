# -*- coding: utf-8 -*-

"""
@author: otll
@time: 2023/11/11
"""

from tool import Crawler_Base


class Crawls(Crawler_Base):
    """
    网易新闻 热榜
    """

    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://m.163.com/fe/api/hot/news/flow'

    def crawls_parse(self):
        result_list = []
        first_num = 0
        for each in self.crawls_getresponse().json().get('data', {}).get('list', []):
            first_num += 1
            hot_dic = dict()
            hot_dic["h_id"] = each.get("skipID", "")
            hot_dic["title"] = each.get("title", "")
            hot_dic["desc"] = ""
            hot_dic["pic"] = each.get("imgsrc", "")
            hot_dic["owner"] = each.get("source", "")
            hot_dic["index"] = first_num
            hot_dic["url"] = f"https://www.163.com/dy/article/{hot_dic['h_id']}.html" if hot_dic.get('h_id') else ""
            hot_dic["mobileUrl"] = each.get("url", "")

            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list


if __name__ == '__main__':
    info = Crawls().crawls_run()
    print(info)
