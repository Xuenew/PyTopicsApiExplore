from flask import Blueprint, render_template, request
from tool import get_comment_xiaoyuzhou
from tool import Base_Back_Result

xiaoyuzhou = Blueprint('xiaoyuzhou', __name__)


# 查询token的情况是否存在和业务使用情况 至少得有一个业务，不会只有token没有业务的情况
@xiaoyuzhou.route('/xyz_lucky_json', methods=['get', 'post'])
def xyz_lucky():

    Back_Resut = Base_Back_Result.copy()

    if request.method == "GET":
        token = request.args.get("token", "")
        episode = request.args.get("episode", "")

    if not token or not episode:  # 没有输入token或者token_type的情况
        Back_Resut["status"] = -1
        Back_Resut["err_msg"] = "请输入正确的episode或联系作者xyy"
        return Back_Resut
    uid_list = []
    token_type_info = []
    response = get_comment_xiaoyuzhou(episode)  # 这里默认拿的很多就不翻页暂时 可以翻页的应该
    for each_data in response.json().get("data",[]):
        each = dict()
        each["name"] = each_data.get("author", {}).get("nickname", "")  # 昵称
        each["uid"] = each_data.get("author", {}).get("uid", "")  # 用户ID
        each["comment"] = each_data["text"]  # 评论
        each["img"] = each_data.get("author", {}).get("avatar", {}).get("picture", {}).get("picUrl", "")  # 头像
        each["probability"] = "1"
        each["pubtime"] = each_data["createdAt"]  #  发布时间
        each["likeCount"] = each_data["likeCount"]  # 点赞数
        if each["uid"] not in uid_list:
            uid_list.append(each["uid"])

            token_type_info.append(each)

    Back_Resut["res_inf"] = {
        "status": 200,  # 用户token_type错误或未开通服务
        "lis": token_type_info
    }
    print(token,episode)
    return Back_Resut


# 查询token的情况是否存在和业务使用情况 至少得有一个业务，不会只有token没有业务的情况
@xiaoyuzhou.route('/xyz_lucky', methods=['get', 'post'])
def xyz_lucky_html():
    Back_Resut = Base_Back_Result.copy()

    if request.method == "GET":
        token = request.args.get("token", "")
        episode = request.args.get("episode", "")

    if not token or not episode:  # 没有输入token或者token_type的情况
        Back_Resut["status"] = -1
        Back_Resut["err_msg"] = "请输入正确的token/episode或联系作者xyy"
        # return Back_Resut
        return "请输入正确的token或联系作者xyy"
    if token not in ["65473dd8d4115bf7390d7b12","61bd3d92e1ba7b4ecec1f865"]:
        # 61bd3d92e1ba7b4ecec1f865 野声
        # 65473dd8d4115bf7390d7b12 豆米
        Back_Resut["status"] = -1
        Back_Resut["err_msg"] = "请输入正确的token或联系作者xyy"
        # return Back_Resut
        return "请输入正确的token或联系作者xyy"
    return render_template("xiaoyuzhou/xiaoyuzhou_choujiang_lucky.html",token=token,episode=episode)






# 测试可以打开 提交前要注释这里
# if __name__ == '__main__':
#     # token_type_info = redis_noremal_hash(type_="hexists", keyname="12345", filed="redbull1", db=1)
#     token_type_info = redis_noremal_hash(type_="hget", keyname="12345", filed="redbull", db=1)
#     print(token_type_info)