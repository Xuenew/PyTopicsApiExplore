# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/7/30

import json

from flask import Flask
from flask import request
from crawls.back_you_want import back_you_want

app = Flask(__name__)


@app.route('/')
def run():
    return 'hello PyTopicsApiExplore!'


@app.route('/thanks')
def thanks():
    return 'hello djn lpy xyy! just do it.'


@app.route('/board_new', methods=['get', 'post'])
def board_new():
    """
    board_type config配置里面榜单的ID
    :return: [{},{}]，默认不填写返回所有榜单[[{},{}],[{},{}],[{},{}]]
    """
    if request.method == 'POST':
        board_type = request.form.get("board_type",0)
    elif request.method == 'GET':
        board_type = request.args.get("board_type", 0)
    # print(board_type)
    return json.dumps(back_you_want(choose_board_type=int(board_type)))


def run_():
    app.run(host="0.0.0.0", port=5000)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
