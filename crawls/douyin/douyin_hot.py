from tool import Crawler_Base


class Crawls(Crawler_Base):

    """
    爬取抖音热榜
    """
    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://aweme.snssdk.com/aweme/v1/hot/search/list/'

    def crawls_parse(self):
        """
        解析抖音热点榜
        """
        result_list = []
        for each in self.crawls_getresponse().json()['data']['word_list']:
            hot_dic = dict()
            hot_dic["h_id"] = each.get("group_id","")
            hot_dic["title"] = each.get("word", "")
            hot_dic["desc"] = ""
            hot_dic["pic"] = each.get("word_cover", {}).get("url_list", [])[0]
            hot_dic["owner"] = ""
            hot_dic["data"] = ""
            hot_dic["hot"] = each.get("hot_value", "")
            hot_dic["index"] = each.get("position", "")
            hot_dic["url"] = "https://www.douyin.com/hot/{}".format(each.get("sentence_id", ""))
            hot_dic["mobileUrl"] = "https://www.douyin.com/hot/{}".format(each.get("sentence_id", ""))
            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list

if __name__ == '__main__':

    info = Crawls().crawls_run()
    print(info)
