# -*- coding:utf-8 -*-
# 从django.http命名空间引入一个HttpResponse的类
import base64
import sys

import simplejson
from captcha.helpers import captcha_image_url
# 验证码模块
from captcha.models import CaptchaStore
from django.conf import settings
from django.conf import settings as django_settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from vmm.model.forms import user_login
from vmm.model.forms import user_regist
# 引用VMware相关库
# import tools.cli as cli
# 引用模型和表单
from vmm.model.models import users
from vmm.model.token import Token

# 验证码模块

reload(sys)
sys.setdefaultencoding('utf8')

token_confirm = Token(settings.SECRET_KEY)


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
                isadmin = db_info.values_list('isadmin')[0][0]  # 返回一个布尔类型！
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
        data = {"ok": "true"}
        # return HttpResponseRedirect('/login/')  # 跳转到index界面
    except KeyError:
        pass

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





# 注册账号

def userregist(request):
    if request.method == 'POST':
        regist_info = user_regist(request.POST)

        if regist_info.is_valid():
            input_id = regist_info.cleaned_data["user_id"]
            db_user_id = users.objects.filter(user_id=input_id)
            user_info = users.objects.all()
            # for user in user_info:
            #     if user.user_id==input_id:
            #         if user.user_password=="":
            #             b=1
            #             break
            #         else:
            #             b=0
            #             break
            # if b==0:
            #     print (users.user_password)
            #     ss = {"reg": "已有密码"}
            #     return HttpResponse(simplejson.dumps(ss, ensure_ascii=False), content_type="application/json")
            # else:
            if db_user_id:

                if regist_info.cleaned_data["user_password1"] == regist_info.cleaned_data["user_password2"]:

                    encryption = base64.encodestring(input_id)

                    if users.objects.filter(email=regist_info.cleaned_data["email"]):
                        from_email = settings.DEFAULT_FROM_EMAIL

                        token = token_confirm.generate_validate_token(input_id)
                        message = "\n".join([u'{0},欢迎加入我的博客'.format(input_id), u'请访问该链接，完成用户验证:',
                                             '/'.join([django_settings.DOMAIN, 'active_user', token])])

                        msg = EmailMultiAlternatives("注册成功", message, from_email, [regist_info.cleaned_data["email"]])
                        msg.send()
                    db_info_renew = users.objects.get(user_id=input_id)
                    db_info_renew.user_id = regist_info.cleaned_data["user_id"]
                    db_info_renew.user_password = regist_info.cleaned_data["user_password1"]
                    db_info_renew.real_name = regist_info.cleaned_data["real_name"]
                    db_info_renew.email = regist_info.cleaned_data["email"]
                    db_info_renew.isadmin = False
                    db_info_renew.is_active = False
                    db_info_renew.save()
                    ss = {"reg": "注册"}
                    return HttpResponse(simplejson.dumps(ss, ensure_ascii=False), content_type="application/json")

                else:
                    ss = {"reg": "密码不匹配"}
                    return HttpResponse(simplejson.dumps(ss, ensure_ascii=False), content_type="application/json")
            else:
                ss = {"reg": "该账号不能注册"}
                return HttpResponse(simplejson.dumps(ss, ensure_ascii=False), content_type="application/json")
        else:
            print (regist_info.data)
            ss = {"reg": "输入错误"}
            return HttpResponse(simplejson.dumps(ss, ensure_ascii=False), content_type="application/json")

    else:
        ss = {"reg": "页面"}
        return HttpResponse(simplejson.dumps(ss, ensure_ascii=False), content_type="application/json")


# 邮箱验证函数
def active_user(request, token):
    """
the view function is used to accomplish the user register confirm,only after input the link
that sent to the register email,user can login the site normally.
:param request:
:param activate_key:the paragram is gotten by encrypting username when user register
:return:
    """
    try:
        user_id = token_confirm.confirm_validate_token(token)
    except:
        return HttpResponse(u'对不起，验证链接已经过期')
    try:
        user = users.objects.get(user_id=user_id)
    except users.DoesNotExist:
        return HttpResponse(u'对不起，您所验证的用户不存在，请重新注册')
    user.isactive = True
    user.save()
    tp = loader.get_template("re_success.html")
    html = tp.render()
    return HttpResponse(html)





def change(request):
    if request.method == 'POST':
        regist_info = user_regist(request.POST)
        if regist_info.is_valid():
            input_id = regist_info.cleaned_data["user_id"]
            db_user_id = users.objects.filter(user_id=input_id)
            if db_user_id:
                if regist_info.cleaned_data["user_password1"] == regist_info.cleaned_data["user_password2"]:
                    db_info_renew = users.objects.get(user_id=input_id)
                    db_info_renew.user_id = regist_info.cleaned_data["user_id"]
                    db_info_renew.user_password = regist_info.cleaned_data["user_password1"]
                    db_info_renew.real_name = regist_info.cleaned_data["real_name"]
                    db_info_renew.email = regist_info.cleaned_data["email"]
                    db_info_renew.mobile = regist_info.cleaned_data["mobile"]
                    db_info_renew.isadmin = False
                    db_info_renew.is_active = False
                    db_info_renew.comment = regist_info.cleaned_data["comment"]
                    db_info_renew.save()
                    return HttpResponse("修改成功")
                else:
                    return HttpResponse("密码不匹配")
            else:
                return HttpResponse("该账号不存在")
        else:
            return HttpResponse("输入错误字段")
    else:
        return HttpResponse("页面不存在")