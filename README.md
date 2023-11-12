# 开发注意
config配置文件忽略不上传，保留config_bs文件字段，注意实际本地部署的时候新建一个config.py文件包含实际环境，内容和config_bs.py一致，
# 平台路径填写到 config.py

# PyTopicsApiExplore

# 注意 python3.8+
```python
{
    "status": -1, # 状态码 200 正常 -1 有问题
    "erro_msg": "",
    "get_time":'2023-11-11 16:43:00',
    "result_info": [[],[]]
}
```

```sh
*/5 * * * * /bin/bash /home/temp/PyTopicsApiExplore/hot_reload.sh
*/10 * * * * /bin/bash /home/temp/PyTopicsApiExplore/hot_api_crontab.sh
```