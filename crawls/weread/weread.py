# -*- coding: utf-8 -*-

"""
@author: otll
@time: 2023/11/11
"""
from tool import Crawler_Base
from utils.getWereadID import getWereadID


class Crawls(Crawler_Base):
    """
    微信读书 飙升榜
    """

    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://weread.qq.com/web/bookListInCategory/rising?rank=1'

    def crawls_parse(self):
        result_list = []
        first_num = 0
        for each in self.crawls_getresponse().json().get('books', []):
            tmp_data = each.get('bookInfo', {})
            first_num += 1
            hot_dic = dict()
            hot_dic["h_id"] = tmp_data.get("bookId", "")
            hot_dic["title"] = tmp_data.get("title", "")
            hot_dic["desc"] = tmp_data.get("title", "")
            hot_dic["pic"] = tmp_data.get("cover", "").replace("s_", "t9_")
            hot_dic["owner"] = tmp_data.get("author", "")
            hot_dic["hot"] = each.get("readingCount", "")
            hot_dic["index"] = first_num
            hot_dic["url"] = f"https://weread.qq.com/web/bookDetail/{getWereadID(hot_dic['h_id'])}" if hot_dic.get('h_id') else ""
            hot_dic["mobileUrl"] = f"https://weread.qq.com/web/bookDetail/{getWereadID(hot_dic['h_id'])}" if hot_dic.get('h_id') else ""

            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list


if __name__ == '__main__':
    info = Crawls().crawls_run()
    print(info)
