# -*- coding: utf-8 -*-

"""
@author: otll
@time: 2023/11/11
"""

from tool import Crawler_Base


class Crawls(Crawler_Base):
    """
    原神 最新消息
    """

    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://content-static.mihoyo.com/content/ysCn/getContentList?pageSize=50&pageNum=1&channelId=10'

    def crawls_parse(self):
        result_list = []
        first_num = 0
        for each in self.crawls_getresponse().json().get('data', {}).get('list', []):
            first_num += 1
            hot_dic = dict()
            hot_dic["h_id"] = each.get("id", "")
            hot_dic["title"] = each.get("title", "")
            hot_dic["desc"] = ""
            try:
                hot_dic["pic"] = each.get("ext", "")[1].get("value", "")[0].get("url", "")
            except:
                hot_dic["pic"] = ""
            hot_dic["index"] = first_num
            hot_dic["url"] = f"https://ys.mihoyo.com/main/news/detail/{hot_dic['h_id']}" if hot_dic.get('h_id') else ""
            hot_dic["mobileUrl"] = f"https://ys.mihoyo.com/main/m/news/detail/{hot_dic['h_id']}" if hot_dic.get('h_id') else ""

            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list


if __name__ == '__main__':
    info = Crawls().crawls_run()
    print(info)
