"""
1. 爬虫的字段保持一致
2. 默认都是str
3. 必填的字段可以为空但一定要有，建议以下字段都填如果没有就置空

"""
example = {
            "h_id": "",  # 内容ID 非必填 不保留数据库
            "title": "",  # 标题 必填留数据库 优先展示title
            "desc": "",  # 简介 非必填 不保留数据库
            "pic": "",  # 图片 非必填 不保留数据库
            "owner": "",  # 作者 非必填 不保留数据库
            "data": "",  # 相关的数据 非必填 不保留数据库
            "hot": "",  # 热度 非必填 不保留数据库
            "index": "",  # 排名 必填留数据库
            "url": "",  # pc端链接 必填留数据库
            "mobileUrl": "",  # 手机端调起链接 必填留数据库
          }
