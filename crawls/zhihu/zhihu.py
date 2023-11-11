import json
import re

from tool import Crawler_Base
from tool import UserAgent_Base

class Crawls(Crawler_Base):
    """
    爬取排行榜
    """

    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = "https://www.zhihu.com/hot"
        self.headers = {
            'authority': 'www.zhihu.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            # 'user-agent': UserAgent_Base().random(),
        }

    def crawls_parse(self):
        """
        解析知乎排行榜
        """
        pattern = r'<script id="js-initialData" type="text/json">(.*?)</script>'
        # print(self.crawls_getresponse().text)
        data_info = json.loads("".join(re.findall(pattern, self.crawls_getresponse().text)))

        # print(json.dumps(data_info))
        result_list = []
        first_num = 0

        for each in data_info.get("initialState",{}).get("topstory",{}).get("hotList", []):
            first_num += 1
            hot_dic = dict()
            hot_dic["h_id"] = "".join(re.findall(r'question/(\d+)', each.get("target", {}
                                                                             ).get("link", {}).get("url", "")))
            hot_dic["title"] = each.get("target", {}).get("titleArea", {}).get("text", "")
            hot_dic["desc"] = each.get("target", {}).get("excerptArea", {}).get("text", "")
            hot_dic["pic"] = each.get("target", {}).get("imageArea", {}).get("url", "")
            hot_dic["owner"] = ""
            hot_dic["data"] = ""
            hot_num = "".join(
                    re.findall(r"[\d,/.]", each.get("target", {}).get("metricsArea", {}).get("text", ""))
                        )
            hot_dic["hot"] = float(hot_num) * 10000 if hot_num else ""
            hot_dic["index"] = first_num
            hot_dic["url"] = each.get("target", {}).get("link", {}).get("url", "")
            hot_dic["mobileUrl"] = each.get("target", {}).get("link", {}).get("url", "")
            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list


if __name__ == '__main__':
    info = Crawls().crawls_run()
    print(info)
