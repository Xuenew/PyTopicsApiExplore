from tool import Crawler_Base
from urllib.parse import quote


class Crawls(Crawler_Base):

    """
    爬取微博排行榜
    """
    def __init__(self):
        super(Crawls, self).__init__()
        self.index_url = 'https://weibo.com/ajax/side/hotSearch'

    def crawls_parse(self):
        """
        解析微博排行榜
        """
        result_list = []
        for each in self.crawls_getresponse().json()['data']['realtime']:
            hot_dic = dict()
            hot_dic["h_id"] = each.get("mid","")
            hot_dic["title"] = each.get("word", "")
            hot_dic["desc"] = each.get("note", "")
            hot_dic["pic"] = each.get("pic", "")
            hot_dic["owner"] = each.get("owner", {})
            hot_dic["data"] = each.get("stat", "")
            hot_dic["hot"] = each.get("num", "")
            hot_dic["index"] = each.get("realpos", "")
            search_key = each.get("word", "") or each.get("word_scheme", "")
            hot_dic["url"] = f"https://s.weibo.com/weibo?q={quote(search_key)}&t=31&band_rank=1&Refer=top"
            hot_dic["mobileUrl"] = f"https://s.weibo.com/weibo?q=${quote(search_key)}&t=31&band_rank=1&Refer=top"
            result_list.append(hot_dic)
        # print(self.crawls_getresponse().text)
        return result_list

if __name__ == '__main__':

    info = Crawls().crawls_run()
    print(info)
