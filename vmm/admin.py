# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# 从django.http命名空间引入一个HttpResponse的类
from django.http import HttpResponse
from django.template import loader, Context
from django.contrib import admin
from django.http import HttpResponseRedirect
import simplejson
# Register your models here.
'''
定义一个方法，处理用户的HTTP请求，并给出HTTP回复
'''
def index(request):
    tp = loader.get_template("backend/index.html")
    html = tp.render({"count": 1, "vms": 2})
    return HttpResponse(html)


'''
定义一个方法，处理用户的HTTP请求，并给出HTTP回复
'''


def logout(request):
    try:
        del request.session['member_id']
        return HttpResponseRedirect('/login')  # 跳转到index界面
    except KeyError:
        pass
    data = {"ok": "true"}
    # 返回JSON格式的对象
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False), content_type="application/json")
