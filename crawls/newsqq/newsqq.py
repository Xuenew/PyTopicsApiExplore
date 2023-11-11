# -*- coding: utf-8 -*-

"""
@author: otll
@time: 2023/11/11
"""

from tool import Crawler_Base


class Crawls(Crawler_Base):
    """
    腾讯新闻 热榜
    """

    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://r.inews.qq.com/gw/event/hot_ranking_list?page_size=50'

    def crawls_parse(self):
        result_list = []
        first_num = 0
        for each in self.crawls_getresponse().json().get('idlist', [])[0].get('newslist', [])[1:]:
            first_num += 1
            hot_dic = dict()
            hot_dic["h_id"] = each.get("id", "")
            hot_dic["title"] = each.get("title", "")
            hot_dic["desc"] = each.get("abstract", "")
            hot_dic["pic"] = each.get("miniProShareImage", "")
            hot_dic["hot"] = each.get("readCount", "")
            hot_dic["index"] = first_num
            hot_dic["url"] = f"https://new.qq.com/rain/a/{hot_dic['h_id']}" if hot_dic.get('h_id') else ""
            hot_dic["mobileUrl"] = f"https://view.inews.qq.com/a/{hot_dic['h_id']}" if hot_dic.get('h_id') else ""

            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list


if __name__ == '__main__':
    info = Crawls().crawls_run()
    print(info)
