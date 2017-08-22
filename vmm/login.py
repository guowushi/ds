# -*- coding:utf-8 -*-
# 从django.http命名空间引入一个HttpResponse的类
from django.http import HttpResponse
from django.template import loader, Context
# 引用VMware相关库
import atexit
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import tools.cli as cli
# 引用模型和表单
from vmm.models import users
from vmm.forms import user_login
import simplejson


# 判断用户名，密码是否正确
def verify_user_info(id, password):
    try:
        db_info = users.objects.filter(user_id=id)
        if db_info:
            db_password = str(db_info.values_list('user_password')[0][0])
            if db_password == password:
                return True
            else:
                return False  # 密码错误
        else:
            return False  # 用户id错误
    except:
        return False  # 未知错误


# 登录视图
def login(request):
    try:
        if request.method == 'POST':
            login_info = user_login(request.POST)
            result = {'user_pass': False, 'captche': False}
            if login_info.is_valid():
                if verify_user_info(str(login_info.cleaned_data['user_id']),
                                    str(login_info.cleaned_data['user_password'])):
                    print("验证成功！")
                    result['user_pass'] = True
                    result['captche'] = True
                    # 返回JSON格式的对象
                    return HttpResponse(simplejson.dumps(result, ensure_ascii=False), content_type="application/json")
                else:
                    print("用户名或密码错误！")
                    result['captche'] = True
                    # 返回JSON格式的对象
                    return HttpResponse(simplejson.dumps(result, ensure_ascii=False), content_type="application/json")
            else:
                print("验证码错误！")
                return HttpResponse(simplejson.dumps(result, ensure_ascii=False), content_type="application/json")
        else:
            tp = loader.get_template("login.html")
            html = tp.render({"count": 1, "vms": 2})
            return HttpResponse(html)
    except:
        print("请求url包含错误信息！")


# 验证码视图
def yzhengma():
    pass
