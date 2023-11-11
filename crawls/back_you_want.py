import importlib

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
                    ]


# 调用的模版
def back_you_want():
    """
    返回需要爬取信息
    """
    for each in HOT_FUNCTION_UNIT:
        if each["board_status"] == 1:
            info = importlib.import_module(each["board_path"]).Crawls().crawls_run()
            print(info)
    return ""


if __name__ == '__main__':

    info = back_you_want()

