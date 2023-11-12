import datetime
import json
import pymysql

from crawls.back_you_want import back_you_want
from tool import mysql_normal
from tool import redis_normal
from config import MYSQL_DB
from config import REDIS_DB

"""
10分钟更新一次
"""


def save_to_mysql(result_list,get_time_):  # 保存到数据库

    for each_platform in result_list.get("result_info",[]):
        for each_platform_lis in each_platform["result"]:
            sql = "insert into {}(board_type, index_num, title, pc_url, mobile_url, get_time) values(%s,%s,%s,%s,%s,%s)".format(
                MYSQL_DB["info_table_name"],
            )
            status = mysql_normal(sql=sql, method="insert", db=MYSQL_DB["db"],sql_list=tuple([each_platform_lis["board_type"],
                each_platform_lis["index"],
                pymysql.converters.escape_string(each_platform_lis["title"]),
                pymysql.converters.escape_string(each_platform_lis["url"]),
                pymysql.converters.escape_string(each_platform_lis["mobileUrl"]),
                get_time_]))
    return True


def save_to_redis_need(result:list):  # 保存到redis里的resul精简一下大小
    result_back = []
    for each in result:
        dic = {}
        dic["index"] = each["index"]
        dic["title"] = each["title"]
        dic["url"] = each["url"]
        # dic["mobileUrl"] = each["mobileUrl"]
        result_back.append(dic)
    return result_back


def save_to_redis(result_list, get_time_):  # 保存到redis
    con = redis_normal(db=REDIS_DB["db"])

    for each in result_list["result_info"]:
        # print(each)
        data = {
            "get_time_": get_time_,
            "board_type": each["board_type"],
            "board_title": each["board_title"],
            "board_subtitle": each["board_subtitle"],
            "result": json.dumps(save_to_redis_need(each["result"])),
        }
        con.hmset(each["board_type"], data)
    con.close()
    return True


def run():  # 执行函数
    result_list = back_you_want(choose_board_type=0)  # 默认全拿
    # print(result_list)
    get_time_ = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00") # 执行的当前时间

    save_to_mysql(result_list, get_time_)
    save_to_redis(result_list, get_time_)


if __name__ == '__main__':
    run()
