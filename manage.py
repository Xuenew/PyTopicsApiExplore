# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/7/30

import json

from flask import Flask
from flask import render_template
from flask import request
from flask_cors import CORS
from crawls.back_you_want import back_you_want
from tool import redis_normal_get_now_db  # 获取redis当前的内容
from tool import get_hot_title_ranking  # 获取榜单位次区间变化
from tool import Base_Back_Result
from tool import redis_noremal_gethk_get # 获取key里单独键的value
from tool import redis_noremal_string_get # 获取key的值
from tool import get_search_keywords # 通过关键词搜索获取结果
from urllib.parse import unquote
from management.user import user
from management.xiaoyuzhou import xiaoyuzhou
from config import HOT_FUNCTION_UNIT

app = Flask(__name__)
CORS(app)
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(xiaoyuzhou, url_prefix='/xiaoyuzhou')

@app.route('/')
def run():
    return 'Hello PyTopicsApiExplore!'


@app.route('/thanks')
def thanks():
    return 'hello djn lpy xyy! just do it.'


@app.route('/board_new', methods=['get', 'post'])  # 返回实时的当前的热点信息实时拿
def board_new():
    """
    board_type config配置里面榜单的ID
    :return: [{},{}]，默认不填写返回所有榜单[[{},{}],[{},{}],[{},{}]]
    """
    if request.method == 'POST':
        board_type = request.form.get("board_type", 0)
        back_format = request.form.get("back_format", "json")
    else:
        board_type = request.args.get("board_type", 0)
        back_format = request.args.get("back_format", "json")

    # 返回的信息块 都用 Base_Back_Result模版返回
    Back_Resut = Base_Back_Result.copy()
    try:
        Back_Resut["res_inf"] = back_you_want(choose_board_type=int(board_type))
    except Exception as e:
        Back_Resut["status"] = -1
        Back_Resut["err_msg"] = str(e)
    # 返回的信息块

    if back_format == "json":
        # print(board_type)
        return json.dumps(Back_Resut)

    else:
        return render_template("board_new.html", blocks=Back_Resut["res_inf"])

@app.route('/board_new_db', methods=['get', 'post'])  # 返回实时的当前的热点信息从redis
def board_new_db():
    """
    board_type_lis config配置里面榜单的ID 传入格式 1,2,3,4,5,9
    :return: [{},{}]，默认不填写返回所有榜单[[{},{}],[{},{}],[{},{}]]
    """
    if request.method == 'POST':
        board_type_lis = request.form.get("board_type_lis", 0)
        back_format = request.form.get("back_format", "json")
    else:
        board_type_lis = request.args.get("board_type_lis", 0)
        back_format = request.args.get("back_format", "json")
    # 返回的信息块 都用 Base_Back_Result模版返回
    Back_Resut = Base_Back_Result.copy()
    if board_type_lis:  # 必填 "0"的情况
        try:
            if board_type_lis == "0":
                Back_Resut["res_inf"] = redis_normal_get_now_db(board_type_list=[])
            else:
                Back_Resut["res_inf"] = redis_normal_get_now_db(board_type_list=board_type_lis.split(","))
        except Exception as e:
            Back_Resut["status"] = -1
            Back_Resut["err_msg"] = str(e)
    else:
        Back_Resut["status"] = -1
        Back_Resut["err_msg"] = "board_type_lis 是必填"
    # 返回的信息块

    if back_format == "json":
        return json.dumps(Back_Resut)
    else:
        return render_template("board_new_db.html", blocks=Back_Resut["res_inf"])


@app.route('/board_hot_ranking', methods=['get', 'post'])  # 返回实时的当前的热点信息从redis
def board_hot_ranking():
    """
    board_type_lis config配置里面榜单的ID 传入格式 1,2,3,4,5,9
    :return: [{},{}]，默认不填写返回所有榜单[[{},{}],[{},{}],[{},{}]]
    """
    if request.method == 'POST':
        hot_title = request.form.get("hot_title", 0)
        hot_type = request.form.get("hot_type", 0)
        xhours = request.form.get("hours", 24)
        back_format = request.form.get("back_format", "json")
    else:
        hot_title = request.args.get("hot_title", 0)
        hot_type = request.args.get("hot_type", 0)
        xhours = request.args.get("hours", 24)
        back_format = request.args.get("back_format", "json")

    # 返回的信息块 都用 Base_Back_Result模版返回
    Back_Resut = Base_Back_Result.copy()
    if hot_type and hot_title:
        # print(hot_title)
        try:
            Back_Resut["res_inf"] = get_hot_title_ranking(title=unquote(hot_title), board_type=hot_type, hours=int(xhours))
        except Exception as e:
            Back_Resut["status"] = -1
            Back_Resut["err_msg"] = str(e)
    else:
        Back_Resut["status"] = -1
        Back_Resut["err_msg"] = "hot_type/hot_title 是必填"
    # 返回的信息

    if back_format == "json":
        return json.dumps(Back_Resut)
    else:
        res = Back_Resut["res_inf"]
        board_title = redis_noremal_gethk_get(board_type=hot_type)
        return render_template("index_ranking.html", result=Back_Resut, hot_title=hot_title,
                               board_title=board_title, time_data=[i[1] for i in res], info_data=[i[0] for i in res])


@app.route('/board_hot_words', methods=['get', 'post'])  # 返回热词的接口
def board_hot_words():
    """
    dayType 传入格式 'now', 'yesterday' 'today'
    :return:
    """
    if request.method == 'POST':
        dayType = request.form.get("dayType", "now")
        back_format = request.form.get("back_format", "json")
    else:
        dayType = request.args.get("dayType", "now")
        back_format = request.args.get("back_format", "json")

    Back_Resut = Base_Back_Result.copy()

    if back_format == "json":
        try:
            Back_Resut["res_inf"] = redis_noremal_string_get(task_keyname=dayType)
        except Exception as e:
            Back_Resut["status"] = -1
            Back_Resut["err_msg"] = str(e)
        return json.dumps(Back_Resut)
    else:  # 后续再考虑这里加不加html
        Back_Resut["status"] = -1
        Back_Resut["err_msg"] = "暂时这个功能还没有添加html的页面"


@app.route('/board_keywords_search', methods=['get', 'post'])  # 通过关键词返回搜索的结果
def board_keywords_search():
    """
    :keywords 传入格式 "热辣滚烫"
    :board_type 传入格式 '1' 默认0 全部
    :hours 传入小时 12 代表12小时内
    :return:
    """
    if request.method == 'POST':
        keywords = request.form.get("keywords", "djn")
        board_type = request.form.get("board_type", 0)
        hours = request.form.get("hours", 7)
        back_format = request.form.get("back_format", "json")
    else:
        keywords = request.args.get("keywords", "djn")
        board_type = request.args.get("board_type", 0)
        hours = request.args.get("hours", 7)
        back_format = request.args.get("back_format", "json")

    Back_Resut = Base_Back_Result.copy()

    if back_format == "json":
        try:
            Back_Resut["res_inf"] = get_search_keywords(keywords=keywords, board_type=int(board_type), hours=int(hours))
        except Exception as e:
            Back_Resut["status"] = -1
            Back_Resut["err_msg"] = str(e)
        return json.dumps(Back_Resut)
    else:  # 后续再考虑这里加不加html
        Back_Resut["status"] = -1
        Back_Resut["err_msg"] = "暂时这个功能还没有添加html的页面"


@app.route('/board_allname', methods=['get', 'post'])  # 返回所有榜单列表
def board_allname():
    """
    dayType 传入格式 'now', 'yesterday' 'today'
    :return:
    """
    if request.method == 'POST':
        back_format = request.form.get("back_format", "json")
    else:
        back_format = request.args.get("back_format", "json")

    Back_Resut = Base_Back_Result.copy()

    if back_format == "json":
        try:
            Back_Resut["res_inf"] = [{"board_type": i["board_type"], "board_title": i["board_title"],
                                      "board_subtitle": i["board_subtitle"]}
                                     for i in HOT_FUNCTION_UNIT if i["board_status"]==1]
        except Exception as e:
            Back_Resut["status"] = -1
            Back_Resut["err_msg"] = str(e)
        return json.dumps(Back_Resut)
    else:  # 后续再考虑这里加不加html
        Back_Resut["status"] = -1
        Back_Resut["err_msg"] = "暂时这个功能还没有添加html的页面"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
