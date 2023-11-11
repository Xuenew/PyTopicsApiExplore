import requests

from tool import Crawler_Base


class Crawls(Crawler_Base):

    """
    爬取抖音热榜
    """
    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://aweme.snssdk.com/aweme/v1/chart/music/list/'
        self.data = {
                      "device_platform": "android",
                      "version_name": "13.2.0",
                      "version_code": "130200",
                      "aid": "1128",
                      "chart_id": "6853972723954146568",
                      "count": "100",
                    }

    def crawls_parse(self):
        """
        解析抖音热点榜
        """

        result_list = []
        first_num = 0
        for each in self.crawls_getresponse().json()['music_list']:
            first_num += 1
            heat = each.get("heat", "")
            each = each.get("music_info",{})
            hot_dic = dict()
            hot_dic["h_id"] = each.get("id", "")
            hot_dic["title"] = each.get("title", "")
            hot_dic["desc"] = each.get("author", "")
            hot_dic["pic"] = each.get("cover_large", {}).get("url_list", [])[0]
            hot_dic["owner"] = ""
            hot_dic["data"] = ""
            hot_dic["hot"] = heat
            hot_dic["index"] = first_num
            hot_dic["url"] = "https://www.douyin.com/music/{}".format(each.get("id", ""))
            hot_dic["mobileUrl"] = "https://www.douyin.com/music/{}".format(each.get("id", ""))
            # 播放的地址 each.get("play_url", {}).get("uri", "")
            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list

if __name__ == '__main__':

    info = Crawls().crawls_run()
    print(info)
