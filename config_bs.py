# 热榜平台信息 新增在此补充
HOT_FUNCTION_UNIT = [
                        {
                            "board_type": 1,
                            "board_status": 1,  # 1 正常 -1 异常或暂时有问题
                            "board_name": "bilibili",
                            "board_title": "哔哩哔哩",
                            "board_subtitle": "热门榜",
                            "board_path": "crawls.bilibili.bilibili",
                        },
                        {
                            "board_type": 2,
                            "board_status": 1,  # 1 正常 -1 异常或暂时有问题
                            "board_name": "weibo",
                            "board_title": "微博",
                            "board_subtitle": "热搜榜",
                            "board_path": "crawls.weibo.weibo",
                        },
                        {
                            "board_type": 3,
                            "board_status": 1,  # 1 正常 -1 异常或暂时有问题
                            "board_name": "shaoshupai",
                            "board_title": "少数派",
                            "board_subtitle": "热门文章",
                            "board_path": "crawls.shaoshupai.shaoshupai",
                        },
                        {
                            "board_type": 4,
                            "board_status": 1,  # 1 正常 -1 异常或暂时有问题
                            "board_name": "zhihu",
                            "board_title": "知乎",
                            "board_subtitle": "知乎热榜",
                            "board_path": "crawls.zhihu.zhihu",
                        },
                        {
                            "board_type": 5,
                            "board_status": 1,  # 1 正常 -1 异常或暂时有问题
                            "board_name": "baidu",
                            "board_title": "百度",
                            "board_subtitle": "百度热榜",
                            "board_path": "crawls.baidu.baidu",
                        },
                        {
                            "board_type": 6,
                            "board_status": 1,  # 1 正常 -1 异常或暂时有问题
                            "board_name": "douyin_hot",
                            "board_title": "抖音",
                            "board_subtitle": "抖音热榜",
                            "board_path": "crawls.douyin.douyin_hot",
                        },
                        {
                            "board_type": 7,
                            "board_status": 1,  # 1 正常 -1 异常或暂时有问题
                            "board_name": "douyin_music_hot",
                            "board_title": "抖音",
                            "board_subtitle": "抖音热歌榜",
                            "board_path": "crawls.douyin.douyin_music_hot",
                        },
                        {
                            "board_type": 8,
                            "board_status": 1,  # 1 正常 -1 异常或暂时有问题
                            "board_name": "tieba",
                            "board_title": "贴吧",
                            "board_subtitle": "贴吧热议榜",
                            "board_path": "crawls.tieba.tieba_reyi",
                        },
                    ]

PROXIES = {
            # 代理IP和端口
            "proxyHost": "",
            "proxyPort": "",
            # # 代理隧道验证信息
            "proxyUser": "",
            "proxyPass": "",
            }

MYSQL_DB = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "passwd": "123456",
            "db": "test",
            "charset": "utf8",
            }

REDIS_DB = {
            "host": "127.0.0.1",
            "port": 3306,
            "passwd": "123456",
            "db": "test",

            }

proxy = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": PROXIES["proxyHost"],
    "port": PROXIES["proxyPort"],
    "user": PROXIES["proxyUser"],
    "pass": PROXIES["proxyPass"],
}
proxies = {
    "http": proxy,
    "https": proxy,
}