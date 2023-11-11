from tool import mysql_normal

"""
第一次执行的时候，会初始化mysql和redis
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
                          KEY `区分类别` (`board_type`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""


def test_mysql():
    pass


def test_redis():
    pass


def mysql_init():
    pass


def redis_init():
    pass


if __name__ == '__main__':
    pass
