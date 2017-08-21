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

'''
定义一个方法，处理用户的HTTP请求，并给出HTTP回复
'''


def index(request):
    tp = loader.get_template("login.html")
    html = tp.render({"count": 1, "vms": 2})
    return HttpResponse(html)
