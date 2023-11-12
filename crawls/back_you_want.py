import importlib
import datetime

from config import HOT_FUNCTION_UNIT


# 调用的模版
def back_you_want(choose_board_type: int = 0):
    """
    返回需要爬取信息
    :param choose_board_type 可以指定平台进行调用 传递平台ID
    :return {
        "status": 200,
        "erro_msg": "",
        "get_time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00"),
        "result_info":
            }
    """
    result_info = []
    if choose_board_type: # 可以单选
        for each in HOT_FUNCTION_UNIT:
            if choose_board_type == each["board_type"]:
                if each["board_status"] == -1:
                    return {
                            "status": -1,
                            "error_msg": "平台下架有问题目前",
                            "get_time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00"),
                            "result_info": []
                            }
                else:
                    back_info = importlib.import_module(each["board_path"]).Crawls().crawls_run()
                    result_info.append(
                                        {
                                            "board_type": each["board_type"],
                                            "board_title": each["board_title"],
                                            "board_subtitle": each["board_subtitle"],
                                            "result": [dict(each_dic, **each) for each_dic in back_info]
                                        }
                                       )
                    return {
                        "status": 200,
                        "error_msg": "ok",
                        "get_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00"),
                        # "result_info":[dict(each_dic, **each) for each_dic in back_info]
                        "result_info": result_info
                    }
    else:  # 默认全拿一遍
        for each in HOT_FUNCTION_UNIT:
            if each["board_status"] == 1:
                back_info = importlib.import_module(each["board_path"]).Crawls().crawls_run()
                # print(info)
                result_info.append(
                                    {
                                        "board_type": each["board_type"],
                                        "board_title": each["board_title"],
                                        "board_subtitle": each["board_subtitle"],
                                        "result": [dict(each_dic, **each) for each_dic in back_info]
                                    }
                                   )  # 返回的内容是个list还需要在迭代的合并

    return {
            "status": 200,
            "error_msg": "ok",
            "get_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00"),
            "result_info": result_info
            }


if __name__ == '__main__':
    start_timestamp = datetime.datetime.now().timestamp()
    print("开始时间", start_timestamp)
    info = back_you_want(choose_board_type=0)
    print(len(info))
    print(info)
    print("结束时间 {} 共耗时 {}".format(
        datetime.datetime.now().timestamp(), datetime.datetime.now().timestamp() - start_timestamp))

