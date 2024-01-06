from flask import Blueprint, render_template, request
from tool import redis_noremal_hash
from tool import Base_Back_Result

user = Blueprint('user', __name__)


# 查询token的情况是否存在和业务使用情况 至少得有一个业务，不会只有token没有业务的情况
@user.route('/user_token', methods=['get', 'post'])
def user_token():

    Back_Resut = Base_Back_Result.copy()

    if request.method == 'POST':
        token = request.form.get("token", "")
        token_type = request.form.get("token_type", "")

    else:
        token = request.args.get("token", "")
        token_type = request.args.get("token_type", "")

    if not token or not token_type:  # 没有输入token或者token_type的情况
        Back_Resut["status"] = -1
        Back_Resut["err_msg"] = "请输入正确的token或token_type"
        return Back_Resut



    # 这里是加强的判断不过可以先忽略不用管 耗时会翻倍
    # token_type_info = redis_noremal_hash(type_="hexists", keyname=token, filed=token_type, db=1)
    # if not token_type_info:  # 没有找到这个用户token的情况
    #     Back_Resut["status"] = -1001  # 用户token错误
    #     Back_Resut["err_msg"] = "请输入正确的token或token_type"
    #     return Back_Resut



    token_type_info = redis_noremal_hash(type_="hget", keyname=token, filed=token_type, db=1)
    if not token_type_info:  # 有这个用户但是没有这个类别的情况
        Back_Resut["res_inf"] = {
                            "status": -1002,  # 用户token_type错误或未开通服务
                            "info": token_type_info
                            }
        return Back_Resut
    Back_Resut["res_inf"] = {
        "status": 200,  # 用户token_type错误或未开通服务
        "info": token_type_info
    }
    return Back_Resut


# 对指定token里的业务进行自减操作
@user.route('/user_token_reduce', methods=['get', 'post'])
def user_token_reduce():
    Back_Resut = Base_Back_Result.copy()
    if request.method == 'POST':
        token = request.form.get("token", "")
        token_type = request.form.get("token_type", "")

    else:
        token = request.args.get("token", "")
        token_type = request.args.get("token_type", "")
    if not token or not token_type:
        Back_Resut["status"] = -1
        Back_Resut["err_msg"] = "请输入正确的token或token_type"
        return Back_Resut



    # 这里是加强的判断不过可以先忽略不用管 耗时会翻倍
    # token_type_info = redis_noremal_hash(type_="hget", keyname=token, filed=token_type, db=1)
    # if not token_type_info:  # 有这个用户但是没有这个类别的情况
    #     Back_Resut["res_inf"] = {
    #                         "status": -1002,  # 用户token_type错误或未开通服务
    #                         "info": token_type_info
    #                         }
    #     return Back_Resut



    token_type_info = redis_noremal_hash(type_="hincrby", keyname=token, filed=token_type, db=1, amount=-1)
    # print("token_type_info reduce", token_type_info)
    Back_Resut["res_inf"] = {
        "status": 200,
        "info": token_type_info  # 返回自减之后的值
    }
    return Back_Resut

# 测试可以打开 提交前要注释这里
# if __name__ == '__main__':
#     # token_type_info = redis_noremal_hash(type_="hexists", keyname="12345", filed="redbull1", db=1)
#     token_type_info = redis_noremal_hash(type_="hget", keyname="12345", filed="redbull", db=1)
#     print(token_type_info)