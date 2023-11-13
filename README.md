<div align="center">
<a href="" alt="logo" ><img src="https://github.com/Xuenew/PyTopicsApiExplore/logo/logo.jpg" width="120"/></a>
</div>
<h1 align="center">PyTopicsApiExplore(HOT API)</h1>

<div align="center">

[English待完成](./README.en.md) | [简体中文](./README.md)

🚀「PyTopicsApiExplore」是一个开箱即用的高性能异步[抖音](https://www.douyin.com)|[Bilibili](https://www.bilibili.com)等热榜数据爬取工具，支持API调用，定时存储数据库。


</div>

## 🔊 本项目计划在V2.0.0版本进行在线处理会开启一个新的vue项目。
感兴趣的多多关注本项目，纯粹想交朋友和技术交流。

## 👻介绍

本项目是基于 [Flask](https://github.com/pallets/flask)，[Mysql 8.0]()，[Redis 5.0]()，热榜数据爬取工具，并通过Web端（V2.0）实现在线RSS，热点排名，热点数据爬取API。你可以自己部署或改造本项目实现更多功能。

*一些简单的运用场景：*

*减少各个平台停留的时间，进行数据分析 配合本项目API实现自建等.....*


🛸基于本项目的其他仓库

- [建设中](https://github.com/Xuenew/PyTopicsApiExplore)


## ⚗️技术栈

* [manage.py](https://github.com/Xuenew/PyTopicsApiExplore/manage.py) - [Flask](https://github.com/pallets/flask)

> ***hot_api_crontab.sh:***

- 部署之后服务器定时获取信息通过[config.py](https://github.com/Xuenew/PyTopicsApiExplore/config.py)存储到数据库。

> ***hot_reload.sh:***

- 部署服务后 定时热更新

> ***manage.py:***

- 制作的简易Web程序
> ***API 接口例子***
```http
http://127.0.0.1/board_new?board_type=2 
```

***以上文件的参数大多可在[config.py](https://github.com/Xuenew/PyTopicsApiExplore/config.py)中进行修改***

## 💡项目文件结构

```
.   
├── LICENSE
├── README.md
├── config.py
├── config_bs.py
├── crawls
│  ├── back_you_want.py
│  ├── baidu （众多类似平台）
│  │  └── baidu.py
│  ├── crawls_instructions_sample.py
├── hot_api_crontab.sh
├── hot_reload.sh
├── hotapi_crontab.py
├── logo
├── manage.py
├── requirment.txt
├── tool.py
├── utils
│  ├── PyTopicsApiExploreInit.py
│  └── getWereadID.py
└── uwsgi.ini

```

## ✨功能：

> 🟢 状态正常
> 🟠 可能失效


| **站点** | **类别** | **平台ID** | **路径名称**              | **状态** |
|--------|--------|----------|-----------------------|-----|
| 哔哩哔哩   | 热门榜    | 1        | bilibili.bilibili     | 🟢  |
| 微博     | 热搜榜    | 2        | weibo.weibo           | 🟢  |
| 知乎     | 热榜     | 4        | zhihu.zhihu           | 🟢  |
| 百度     | 热搜榜    | 5        | baidu.baidu           | 🟢  |
| 抖音     | 热点榜    | 6        | douyin.douyin_hot     | 🟢  |
| 抖音     | 热歌榜    | 7        | douyin_music_hot      | 🟢  |
| 百度贴吧   | 热议榜    | 8        | tieba.tieba           | 🟢  |
| 少数派    | 热榜     | 3        | shaoshupai.shaoshupai | 🟢  |
| 澎湃新闻   | 热榜     | 9        | thepaper.thepaper     | 🟢  |
| 今日头条   | 热榜     | 10       | toutiao               | 🟢  |
| 36 氪   | 热榜     | 11       | kr36.kr36             | 🟢  |
| 稀土掘金   | 热榜     | 12       | juejin.juejin         | 🟢  |
| 腾讯新闻   | 热点榜    | 13       | newsqq.newsqq         | 🟢  |
| 网易新闻   | 热点榜    | 14       | netease.netease       | 🟢  |
| 英雄联盟   | 更新公告   | 15       | lol.lol               | 🟢  |
| 原神     | 最新消息   | 16       | genshin.genshin       | 🟢  |
| 微信读书   | 飙升榜    | 18       | weread.weread         | 🟢  |
| 快手     | 热榜     | 19       | kuaishou.kuaishou     | 🟢  |
| 历史上的今天 | 指定日期   | 20       | calendar.calendar     | 🟠  |

---

## 🤦‍待办清单：

> 💡欢迎提出建议或直接提交PR至此仓库 づ￣3￣）づ╭❤～

- [ ] 对其他平台添加支持，如：抖音明星榜

---

## 🗺️支持的提交格式：

> 💡提示：包含但不仅限于以下例子，如果遇到热榜解析失败请开启一个新 [issue](https://github.com/Xuenew/PyTopicsApiExplore/issues)

- 哔哩哔哩热榜链接

```text
https://api.bilibili.com/x/web-interface/ranking/v2
```


## 🛰️API文档

> 💡提示：也可以在manage.py的代码注释中查看接口文档


***API演示：***

- 热榜数据(实时获取，ID以文档的为准)
```http request
http://127.0.0.1/board_new?board_type=2
```




## 💻部署(方式一 ubuntu20.04)

> 💡注意：python3.8+版本 前提mysql8.0 和redis都已经安装好了哈

-  安装服务以及建立路径
```bash
mkdir -p /home/temp ;mkdir -p /data/log/temp/;cd /home/temp ;git init;git clone git@github.com:Xuenew/PyTopicsApiExplore.git
```
- 安装环境 (推荐用python虚拟环境) nodejs/uwsgi/nginx
```bash
apt install nodejs -y
apt install nginx -y
apt install python3.8-venv -y
python3 -m venv /home/temp/env_pytopicsapiexplore
pip install uwsgi
```
- 安装依赖
```bash
/home/temp/env_pytopicsapiexplore/bin/pip install -r /home/temp/PyTopicsApiExplore/rerequirment.txt
```
- 初始化数据库 每次热更新也会执行
```bash
/home/temp/env_pytopicsapiexplore/bin/python /home/temp/PyTopicsApiExplore/utils/PyTopicsApiExploreInit.py
```
- 部署定时任务
```bash
# 热更新
*/5 * * * * /bin/bash /home/temp/PyTopicsApiExplore/hot_reload.sh 
# 定时采集
*/10 * * * * /bin/bash /home/temp/PyTopicsApiExplore/hot_api_crontab.sh
```

> 部署web服务(方式1 公网) （uwsgi+nginx）
1) nginx配置 
```bash
cd /etc/nginx/conf.d;vim pytopicsapiexplore.conf
```
```
# 配置如下
server {
        # 监听的端口号,改成什么就是用什么端口访问服务器 ，默认是80
        listen 80;
        # 域名或公网ip ！！！注意这里要改哈
        server_name your domain; 
        charset utf-8;
        # 静态文件访问的url（此处没有）
        # 发送所有非静态文件请求到flask服务器
        location / {
        include uwsgi_params;
        uwsgi_connect_timeout 40;
        # 需要与之前uwsgi配置一样
        uwsgi_pass 127.0.0.1:5000;

        }
}
```
2) uwsgi配置和启动 [uwsgi配置](https://github.com/Xuenew/PyTopicsApiExplore/uwsgi.ini) 
```bash
/usr/local/bin/uwsgi --ini uwsgi.ini
```
3) nginx 启动
```bash
service nginx restart
```

- 部署web服务(方式2 本地) 
```angular2html
flask --app manage.py run -h0.0.0.0 -p5000
```



## ❤️ 贡献者

[![](https://github.com/otll.png?size=50)](https://github.com/otll)
[![](https://github.com/L-dongjianing.png?size=50)](https://github.com/L-dongjianing)

## 免责声明

- 本项目提供的 `API` 仅供开发者进行技术研究和开发测试使用。使用该 `API` 获取的信息仅供参考，不代表本项目对信息的准确性、可靠性、合法性、完整性作出任何承诺或保证。本项目不对任何因使用该 `API` 获取信息而导致的任何直接或间接损失负责。本项目保留随时更改 `API` 接口地址、接口协议、接口参数及其他相关内容的权利。本项目对使用者使用 `API` 的行为不承担任何直接或间接的法律责任
- 本项目并未与相关信息提供方建立任何关联或合作关系，获取的信息均来自公开渠道，如因使用该 `API` 获取信息而产生的任何法律责任，由使用者自行承担
- 本项目对使用 `API` 获取的信息进行了最大限度的筛选和整理，但不保证信息的准确性和完整性。使用 `API` 获取信息时，请务必自行核实信息的真实性和可靠性，谨慎处理相关事项
- 本项目保留对 `API` 的随时更改、停用、限制使用等措施的权利。任何因使用本 `API` 产生的损失，本项目不负担任何赔偿和责任


[MIT License](https://github.com/Xuenew/PyTopicsApiExplore/LICENSE)

> Start: 2023/11/10
> GitHub: [@Xuenew](https://github.com/Xuenew)
