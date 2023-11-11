# -*- coding: utf-8 -*-

"""
@author: otll
@time: 2023/11/11
"""

from tool import Crawler_Base


class Crawls(Crawler_Base):

    """
    澎湃
    """
    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc'

    def crawls_parse(self):

        result_list = []
        first_num = 0
        for each in self.crawls_getresponse().json().get('data', {}):
            first_num += 1
            hot_dic = dict()
            hot_dic["h_id"] = each.get("ClusterId", "")
            hot_dic["title"] = each.get("Title", "")
            hot_dic["desc"] = ""
            hot_dic["index"] = first_num
            hot_dic["url"] = f"https://www.thepaper.cn/newsDetail_forward_{hot_dic['h_id']}" if hot_dic.get('h_id') else ""
            hot_dic["mobileUrl"] = f"https://m.thepaper.cn/newsDetail_forward_{hot_dic['h_id']}" if hot_dic.get('h_id') else ""

            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list


if __name__ == '__main__':
    info = Crawls().crawls_run()
    print(info)
