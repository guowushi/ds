# -*- coding:utf-8 -*-
# 从django.http命名空间引入一个HttpResponse的类
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader, Context

# 验证码模块
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
# 验证码模块

# 引用VMware相关库
import atexit
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
# import tools.cli as cli
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
    # try:
    if request.method == 'POST':
        login_info = user_login(request.POST)
        result = {'user_pass': False, 'captcha': False, 'isadmin': False}

        if login_info.is_valid():
            if verify_user_info(str(login_info.cleaned_data['user_id']),
                                str(login_info.cleaned_data['user_password'])):
                print("验证成功！")
                result['user_pass'] = True
                result['captcha'] = True
                request.session['user_id'] = str(login_info.cleaned_data['user_id'])  # 创建session
                # 判断用户权限
                db_info = users.objects.filter(user_id=request.session.get('user_id'))
                isadmin = db_info.values_list('isadmin')[0][0]     #返回一个布尔类型！
                if isadmin:
                    result['admin'] = True
                    # 返回JSON格式的对象
                    return HttpResponse(simplejson.dumps(result, ensure_ascii=False), content_type="application/json")
                    # return HttpResponseRedirect('/backend/index/')
                else:
                    # 返回JSON格式的对象
                    return HttpResponse(simplejson.dumps(result, ensure_ascii=False), content_type="application/json")
                    # return HttpResponseRedirect('/front/index/')
            else:
                print("用户名或密码错误！")
                result['captcha'] = True
                # 返回JSON格式的对象
                return HttpResponse(simplejson.dumps(result, ensure_ascii=False), content_type="application/json")
        else:
            print(login_info.cleaned_data)
            print("验证码错误！")
            return HttpResponse(simplejson.dumps(result, ensure_ascii=False), content_type="application/json")
    else:
        hashkey = CaptchaStore.generate_key()
        imgage_url = captcha_image_url(hashkey)
        tp = loader.get_template("login.html")
        html = tp.render({"hashkey": hashkey, "imgage_url": imgage_url})
        return HttpResponse(html)
        # except:
        #     print("请求url包含错误信息！")

'''
定义一个方法，处理用户退出登录！
'''
def logout(request):
    try:
        del request.session['user_id']
        return HttpResponseRedirect('/login/')  # 跳转到index界面
    except KeyError:
        pass
    data = {"ok": "true"}
    # 返回JSON格式的对象
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False), content_type="application/json")






# 验证码视图
def captcha_refresh(request):
    """  Return json with new captcha for ajax refresh request """
    if not request.is_ajax():  # 只接受ajax提交
        raise '404'

    new_key = CaptchaStore.generate_key()
    to_json_response = {
        'key': new_key,
        'image_url': captcha_image_url(new_key),
    }
    return HttpResponse(simplejson.dumps(to_json_response, ensure_ascii=False), content_type='application/json')
