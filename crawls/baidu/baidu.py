import json
import re

from tool import Crawler_Base
from tool import UserAgent_Base
from urllib.parse import quote

class Crawls(Crawler_Base):
    """
    爬取排行榜
    """

    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = "https://top.baidu.com/board?tab=realtime"


    def crawls_parse(self):
        """
        解析百度排行榜
        """
        pattern = r'<!--s-data:(.*?)-->'
        # print(self.crawls_getresponse().text)
        data_info = json.loads("".join(re.findall(pattern, self.crawls_getresponse().text)))

        # print(json.dumps(data_info))
        result_list = []

        for each in data_info.get("data", {}).get("cards", [])[0]["content"]:
            hot_dic = dict()
            hot_dic["h_id"] = ""
            hot_dic["title"] = each.get("query", "")
            hot_dic["desc"] = each.get("desc", "")
            hot_dic["pic"] = each.get("img", "")
            hot_dic["owner"] = ""
            hot_dic["data"] = ""
            hot_dic["hot"] = each.get("hotScore", "")
            hot_dic["index"] = str(int(each.get("index", ""))+1)
            hot_dic["url"] = "https://www.baidu.com/s?wd={}".format(quote(each.get("query", "")))
            hot_dic["mobileUrl"] = each.get("url", "")
            if not each.get("isTop", ""):
                result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list


if __name__ == '__main__':
    info = Crawls().crawls_run()
    print(info)
