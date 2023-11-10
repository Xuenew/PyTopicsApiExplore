from tool import Crawler_Base


class Crawls(Crawler_Base):

    """
    爬取少数派
    """
    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://sspai.com/api/v1/article/tag/page/get?limit=40&tag=%E7%83%AD%E9%97%A8%E6%96%87%E7%AB%A0'

    def crawls_parse(self):
        """
        解析少数派热门文章
        """
        result_list = []
        first_num = 0
        for each in self.crawls_getresponse().json()['data']:
            first_num += 1
            hot_dic = dict()
            hot_dic["h_id"] = each.get("id","")
            hot_dic["title"] = each.get("title", "")
            hot_dic["desc"] = each.get("summary", "")
            banner = each.get("banner", "")
            hot_dic["pic"] = f"https://cdn.sspai.com/{banner}"
            hot_dic["owner"] = each.get("author", {})
            hot_dic["data"] = each.get("stat", "")
            hot_dic["hot"] = each.get("like_count", "")
            hot_dic["index"] = first_num
            hot_dic["url"] = "https://sspai.com/post/{}".format(hot_dic["h_id"])
            hot_dic["mobileUrl"] = "https://sspai.com/post/{}".format(hot_dic["h_id"])
            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list

if __name__ == '__main__':

    info = Crawls().crawls_run()
    print(info)
