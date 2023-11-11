# -*- coding: utf-8 -*-

"""
@author: otll
@time: 2023/11/11
"""

from tool import Crawler_Base


class Crawls(Crawler_Base):
    """
    英雄联盟 更新公告
    """

    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://apps.game.qq.com/cmc/zmMcnTargetContentList?page=1&num=16&target=24&source=web_pc'

    def crawls_parse(self):
        result_list = []
        first_num = 0
        for each in self.crawls_getresponse().json().get('data', {}).get('result', []):
            first_num += 1
            hot_dic = dict()
            hot_dic["h_id"] = each.get("iDocID", "")
            hot_dic["title"] = each.get("sTitle", "")
            hot_dic["desc"] = ""
            hot_dic["pic"] = f"https:{each.get('sIMG', '')}" if each.get('sIMG', '') else ""
            hot_dic["owner"] = each.get("sAuthor", "")
            hot_dic["hot"] = each.get("iTotalPlay", "")
            hot_dic["index"] = first_num
            hot_dic["url"] = f"https://lol.qq.com/news/detail.shtml?docid={hot_dic['h_id']}" if hot_dic.get('h_id') else ""
            hot_dic["mobileUrl"] = f"https://lol.qq.com/news/detail.shtml?docid={hot_dic['h_id']}" if hot_dic.get('h_id') else ""

            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list


if __name__ == '__main__':
    info = Crawls().crawls_run()
    print(info)
