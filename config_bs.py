# 实际用的时候把文件名称改为 config.py

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