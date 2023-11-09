from tool import crawaller_base

class crawls(crawaller_base):
    def __init__(self):
        super(crawls, self).__init__()
        self.index_url = 'https://api.bilibili.com/x/web-interface/ranking/v2'


    def crawls_parse(self):
        print(self.crawls_getresponse().text)
        


if __name__ == '__main__':
    info = crawls().crawls_run()
