import datetime
import json
import random

import pymysql
import requests

from crawls.back_you_want import back_you_want
from tool import mysql_normal
from tool import redis_normal
from tool import get_x_hours_ago
from tool import md5_use
from tool import get_min_time
from config import MYSQL_DB
from config import REDIS_DB
from config import DELETE_TIME_DAYS  # 用于定时执行删除库操作
from config import CRONTAB_DELAY_  # 用于计算间隔算在榜时间
from retrying import retry

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


def delet_to_mysql():  # 定时删除数据库的数据
    get_time_ = get_x_hours_ago(hours=DELETE_TIME_DAYS)

    sql = "delete from {} where get_time<%s".format(
        MYSQL_DB["info_table_name"],
    )
    status = mysql_normal(sql=sql, method="do", db=MYSQL_DB["db"],sql_list=tuple([get_time_]))
    return True


def save_to_redis_need(result: list, each_boardinfo: dict, get_time_: str):  # 保存到redis里的resul精简一下大小
    result_back = []
    for each in result:
        dic = {}
        dic["index"] = each["index"]
        dic["title"] = each["title"]
        dic["url"] = each["url"]
        try:
            # 获取最大的排位次和在榜的总时间
            max_index_num, onboard_time, first_onboard_time, max_index_num_time, first_onboard_num = get_onboardtime_and_maxindexnum(
                                                each_boardinfo["board_type"], each["title"], each["index"], get_time_)
            dic["max_index_num"] = max_index_num
            dic["max_index_num_time"] = max_index_num_time
            dic["onboard_time"] = onboard_time
            dic["first_onboard_time"] = first_onboard_time
            dic["first_onboard_num"] = first_onboard_num
        except Exception as e:
            dic["max_index_num_time"] = ""
            dic["first_onboard_num"] = ""
            dic["max_index_num"] = ""
            dic["onboard_time"] = ""
            dic["first_onboard_time"] = ""
        # dic["mobileUrl"] = each["mobileUrl"]
        result_back.append(dic)
    return result_back


def save_to_redis(result_list, get_time_):  # 保存到redis
    con = redis_normal(db=REDIS_DB["db"])
    needs_searchkeywords = get_search_keywordsinfo_frommysql(get_time_)
    # user_need_save_list = []

    for each in result_list["result_info"]:
        save_to_redis_need_list = save_to_redis_need(each["result"], each, get_time_)
        # print(save_to_redis_need_list)
        data = {
            "get_time_": get_time_,
            "board_type": each["board_type"],
            "board_title": each["board_title"],
            "board_subtitle": each["board_subtitle"],
            "result": json.dumps(save_to_redis_need_list),
        }
        con.hmset(each["board_type"], data)

        if str(each["board_type"]) in needs_searchkeywords:  # 发现有匹配到平台类型的在搜索关键词里面
            for each_result in save_to_redis_need_list:  # 匹配到的每一条进行存储
                for each_needs_searchkeywords in needs_searchkeywords[str(each["board_type"])]:
                    if needs_searchkeywords[str(each["board_type"])][each_needs_searchkeywords]["keywords"] in each_result["title"]:
                        each_result["board_type"] = each["board_type"]
                        each_result["get_time_"] = get_time_
                        each_result["uid_needs"] = needs_searchkeywords[str(each["board_type"])][each_needs_searchkeywords]["ulist"]
                        # user_need_save_list.append(each_result)
                        con.lpush(REDIS_DB["user_needs_monitor"], json.dumps(each_result))
    con.close()
    return True


@retry(stop_max_attempt_number=3,wait_fixed=200)
def get_search_keywordsinfo_frommysql(get_time_):  # 从数据表里获取要执行的监控数据
    """
    :param get_time_:
    :return:
    {'2': {'705438613d9b30628a6883970135e5a7': {'ulist': [1, 3, 2], 'keywords': '春运'}, 'b7d672aeeb30c45918420d90a22f5195': {'ulist': [1], 'keywords': '贾玲'}}, '1': {'b7d672aeeb30c45918420d90a22f5195': {'ulist': [1], 'keywords': '贾玲'}}}

    """
    all_result_index_dic = {}

    sql = "SELECT {user_searchkeywords_table}.uid, {user_searchkeywords_table}.board_type, {keywords_table}.keywords FROM {user_searchkeywords_table} JOIN {keywords_table} ON {user_searchkeywords_table}.keyword_id = {keywords_table}.ID where end_time>%s;".format(
        user_searchkeywords_table=MYSQL_DB["user_searchkeywords_table"],
        keywords_table=MYSQL_DB["keywords_table"]
    )
    all_result_index = mysql_normal(sql=sql, method="fetchall", db=MYSQL_DB["db"],
                                    sql_list=tuple([get_time_]))

    # print(all_result_index)
    for each in all_result_index:
        keyword_md5_use = md5_use(each[2])
        if str(each[1]) not in all_result_index_dic:  # 如果这个平台还没有就添加key
            all_result_index_dic[str(each[1])] = {keyword_md5_use: {"ulist": [each[0]], "keywords": each[2]}}
        else:  # 平台已经有的话就添加value 判断关键词在不在

            if keyword_md5_use not in all_result_index_dic[str(each[1])]:
                all_result_index_dic[str(each[1])][keyword_md5_use] = {"ulist": [each[0]], "keywords": each[2]}
            else:
                all_result_index_dic[str(each[1])][keyword_md5_use]["ulist"].append(each[0])
    # print(all_result_index_dic)
    return all_result_index_dic


@retry(stop_max_attempt_number=3,wait_fixed=200)
def get_onboardtime_and_maxindexnum(each_board_type, each_title, each_index, get_time_, rformat="%Y-%m-%d %H:%M:%S"):  # 获取数据库中每一条的在榜时间
    # "select index_num from board_info where board_type=1 and title='出界就死' ORDER BY index_num ASC"  # 测试的例子
    sql = "select index_num,get_time from {} where board_type=%s and title=%s ORDER BY index_num ASC".format(MYSQL_DB["info_table_name"])
    all_result_index = mysql_normal(sql=sql, method="fetchall", db=MYSQL_DB["db"],sql_list=tuple([each_board_type, each_title]))
    # print(all_result_index[0])
    if all_result_index:
        max_index_num = all_result_index[0][0]
        max_index_num_time = all_result_index[0][1].strftime(rformat)  # 最高排次的时间
        onboard_time = CRONTAB_DELAY_ * len(all_result_index) + random.choice(range(1, CRONTAB_DELAY_))  # 添加一个随机时间
        first_onboard_time = min([i[1] for i in all_result_index]).strftime(rformat)
        first_onboard_num = [i for i in all_result_index if i[1].strftime(rformat) == first_onboard_time][0][0]
    else:  # 没有查询的情况就是第一次出现就是10分钟的在榜时间 和最高排次
        max_index_num = each_index
        max_index_num_time = get_time_  # 最高排次的时间 这里可能时间都是整数，后续再说
        onboard_time = CRONTAB_DELAY_ + random.choice(range(1, CRONTAB_DELAY_))  # 添加一个随机时间显得不那么生硬 随机时间通过配置文件来
        first_onboard_time = get_time_  # 没有查到的话第一次就是获取时间
        first_onboard_num = each_index  # 没有查到的话第一次的排名就是
    return max_index_num, onboard_time, first_onboard_time, max_index_num_time, first_onboard_num


def save_hotwords_to_redis():  # 保存热词到redis
    """
    先用other的替代，后期逐步用自己的分词
    :return:
    """
    con = redis_normal(db=REDIS_DB["db"])

    for dayType in ["now","yesterday","today"]:
        # print(each)
        info = get_hotwords(dayType=dayType)
        con.set(dayType, info.text)
    con.close()


def get_hotwords(dayType="now"):  # 这里先用别人的 （0｜0）

    headers = {
        'authority': 'www.entobit.cn',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.entobit.cn',
        'referer': 'https://www.entobit.cn/hot-search/desktop',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'type': 'restful',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    data = {
        # 'dayType': 'now', 'yesterday' 'today'
        'dayType': dayType,
        'dataType': '',
    }

    response = requests.post('https://www.entobit.cn/trending/top/getHotSearchWordcloud.do', headers=headers, data=data)
    return response


def run():  # 执行函数
    save_hotwords_to_redis()   # 保存热榜热词数据到redis

    result_list = back_you_want(choose_board_type=0)  # 默认全拿
    # print(result_list)
    get_time_ = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00")  # 执行的当前时间

    save_to_mysql(result_list, get_time_)  # 保存到数据库热榜数据
    save_to_redis(result_list, get_time_)  # 保存到redis热榜数据 经过计算的热榜数据

    delet_to_mysql()  # 定时删除


if __name__ == '__main__':
    # get_search_keywordsinfo_frommysql("2024-02-05 17:40:00")
    # exit()
    # save_hotwords_to_redis()
    # exit()
    # each_board_type = 1
    # each_title = "出界"
    # each_index = 2
    # info = get_onboardtime_and_maxindexnum(each_board_type, each_title, each_index)
    # print(info)
    # exit()
    run()
