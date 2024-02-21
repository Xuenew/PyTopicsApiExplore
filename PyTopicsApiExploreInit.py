from tool import mysql_normal
from tool import redis_normal
from config import MYSQL_DB
from config import HOT_FUNCTION_UNIT

"""
第一次执行的时候，会初始化mysql和redis
"""

# 创建一个数据库
MYSQL_DATABASE_CREAT_SQL = """
                        CREATE DATABASE hot_board CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

"""

# 创建热榜平台表
MYSQL_TABLE_CREAT_SQL1 = """
                        CREATE TABLE `board_platform` (
                          `id` int NOT NULL AUTO_INCREMENT,
                          `board_type` int NOT NULL,
                          `board_status` int NOT NULL,
                          `board_name` varchar(255) DEFAULT NULL,
                          `board_title` varchar(255) NOT NULL,
                          `board_subtitle` varchar(255) NOT NULL,
                          `board_path` varchar(255) DEFAULT NULL,
                          PRIMARY KEY (`id`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

# 创建热榜详情表
MYSQL_TABLE_CREAT_SQL2 = """
                        CREATE TABLE `board_info` (
                          `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
                          `board_type` int NOT NULL COMMENT '平台类型和表board_platform一致',
                          `index_num` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '排名',
                          `title` varchar(255) DEFAULT NULL COMMENT '热榜标题',
                          `pc_url` text COMMENT 'Pc端的访问链接',
                          `mobile_url` text COMMENT '移动端的访问链接',
                          `get_time` datetime DEFAULT NULL COMMENT '获取时间，索引以此为查询条件',
                          `judge_type` int DEFAULT NULL COMMENT '判断标题的类别是那种，科技类吃瓜类。。。',
                          PRIMARY KEY (`id`),
                          KEY `获取时间` (`get_time`),
                          KEY `区分类别` (`board_type`),
                          KEY `联合标题时间索引` (`title`,`get_time`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

# 创建热榜标题关键词表
MYSQL_TABLE_CREAT_SQL3 = """
                        CREATE TABLE `keywords_table` (
                          `ID` int NOT NULL,
                          `keywords` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '监控的关键词',
                          `keywords_hash` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '关键词的hash唯一值',
                          PRIMARY KEY (`ID`),
                          UNIQUE KEY `keywords_hash` (`keywords_hash`(32))
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
"""

# 创建用户搜索关键词表
MYSQL_TABLE_CREAT_SQL4 = """
                        CREATE TABLE `user_searchkeywords_table` (
                          `id` int NOT NULL AUTO_INCREMENT,
                          `uid` int DEFAULT NULL COMMENT '用户ID',
                          `keyword_id` int DEFAULT NULL COMMENT '关键词的ID md5计算的值',
                          `start_time` datetime DEFAULT NULL COMMENT '用户对于这个关键词的开始监测时间',
                          `end_time` datetime DEFAULT NULL COMMENT '用户对于这个关键词的结束监测时间',
                          `board_type` int DEFAULT NULL COMMENT '对那个平台的监测',
                          PRIMARY KEY (`id`),
                          KEY `keyword_id` (`keyword_id`),
                          CONSTRAINT `user_searchkeywords_table_ibfk_1` FOREIGN KEY (`keyword_id`) REFERENCES `keywords_table` (`ID`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
"""


def test_mysql():  # 检查系统mysql
    # 查询是否建立了数据库
    sql = "SELECT TABLE_SCHEMA,TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA like '{}'".format(MYSQL_DB["db"])
    info = mysql_normal(sql=sql, method="fetchall")
    if info:
        print("mysql数据库已存在 可以继续")
    else:
        print("请创建数据库 hot_board,或者执行初始化函数 mysql_init()")
        info = input("是否执行初始化函数 mysql_init()?(y/n)")
        if info.lower() == "y":
            mysql_init()
        else:
            pass
    return


def test_redis():  # 检查系统redis
    try:
        con = redis_normal()
        con.close()
        print("redis数据库已存在 可以继续")
    except Exception as e:
        info = input("是否执行初始化函数 redis_init()?(y/n)")
        if info.lower() == "y":
            redis_init()
        else:
            pass


# mysql 初始化
def mysql_init():  # 创建mysql部署需要的表和库
    mysql_normal(sql=MYSQL_DATABASE_CREAT_SQL)
    mysql_normal(sql=MYSQL_TABLE_CREAT_SQL1, db=MYSQL_DB["db"])
    mysql_normal(sql=MYSQL_TABLE_CREAT_SQL2, db=MYSQL_DB["db"])
    mysql_normal(sql=MYSQL_TABLE_CREAT_SQL3, db=MYSQL_DB["db"])
    mysql_normal(sql=MYSQL_TABLE_CREAT_SQL4, db=MYSQL_DB["db"])
    print("数据库表初始化完成！进行平台数据插入")


# redis 初始化
def redis_init():  # 创建redis部署需要
    print("请在本地创建redis数据库 或者 阿里云购买云数据库Redis版")


def insert_new_boardinfo(already_exist):
    for each in HOT_FUNCTION_UNIT:
        sql = "insert into {}(board_type,board_status,board_name,board_title,board_subtitle,board_path) values(%s,%s,%s,%s,%s,%s)".format(
            MYSQL_DB["platform_table_name"])
        # print(sql)
        board_type = each["board_type"]
        if board_type not in already_exist:
            board_status = each["board_status"]
            board_name = each["board_name"]
            board_title = each["board_title"]
            board_subtitle = each["board_subtitle"]
            board_path = each["board_path"]
            status = mysql_normal(sql,db=MYSQL_DB["db"],method="insert",sql_list=(board_type, board_status, board_name, board_title, board_subtitle, board_path))


# 平台数据更新
def board_platform_update():
    # 获取所有已经存在的板块类型
    already_exist = mysql_normal(sql="select board_type from {}".format(MYSQL_DB["platform_table_name"]),db=MYSQL_DB["db"],method="fetchall")
    already_exist = [each[0] for each in already_exist]
    # print(already_exist)
    # 插入新的板块类型
    insert_new_boardinfo(already_exist)
    print("平台数据插入完成！开始愉悦的使用 PyTopicsApiExploreInit 吧")


# 初始化
def run_init():
    test_mysql()
    test_redis()
    board_platform_update()  # 每次新增了平台


if __name__ == '__main__':
    run_init()
