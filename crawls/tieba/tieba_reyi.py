from tool import Crawler_Base


class Crawls(Crawler_Base):

    """
    爬取贴吧热议排行榜
    """
    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://tieba.baidu.com/hottopic/browse/topicList'

    def crawls_parse(self):
        """
        解析贴吧热议排行榜
        """
        result_list = []
        for each in self.crawls_getresponse().json()['data']['bang_topic']["topic_list"]:
            hot_dic = dict()
            hot_dic["h_id"] = each.get("topic_id","")
            hot_dic["title"] = each.get("topic_name", "")
            hot_dic["desc"] = each.get("topic_desc", "")
            hot_dic["pic"] = each.get("topic_pic", "")
            hot_dic["owner"] = ""
            hot_dic["data"] = ""
            hot_dic["hot"] = each.get("discuss_num", "")
            hot_dic["index"] = each.get("idx_num", "")
            hot_dic["url"] = each.get("topic_url", "")
            hot_dic["mobileUrl"] = each.get("topic_url", "")
            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list

if __name__ == '__main__':

    info = Crawls().crawls_run()
    print(info)
