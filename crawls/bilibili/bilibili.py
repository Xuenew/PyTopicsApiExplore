from tool import Crawler_Base


class Crawls(Crawler_Base):

    """
    爬取B站排行榜
    """
    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://api.bilibili.com/x/web-interface/ranking/v2'

    def crawls_parse(self):
        """
        解析B站排行榜
        """
        result_list = []
        for each in self.crawls_getresponse().json()['data']['list']:
            hot_dic = dict()
            hot_dic["h_id"] = each.get("bvid","")
            hot_dic["title"] = each.get("title", "")
            hot_dic["desc"] = each.get("desc", "")
            hot_dic["pic"] = each.get("pic", "")
            hot_dic["owner"] = each.get("owner", {})
            hot_dic["data"] = each.get("stat", "")
            hot_dic["hot"] = each.get("stat", {}).get("view", "")
            hot_dic["index"] = each.get("stat", {}).get("his_rank", "")
            hot_dic["url"] = each.get("short_link_v2", "") or "https://b23.tv/{}".format(hot_dic["h_id"])
            hot_dic["mobileUrl"] = "https://m.bilibili.com/video/{}".format(hot_dic["h_id"])
            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list

if __name__ == '__main__':

    info = Crawls().crawls_run()
    print(info)
