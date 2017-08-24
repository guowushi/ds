# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# 从django.http命名空间引入一个HttpResponse的类
from django.http import HttpResponse
from django.template import loader, Context
from django.contrib import admin
from django.http import HttpResponseRedirect
import simplejson

# 引用VMware相关库
import atexit
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim

# 引用模型和表单
from vmm.models import users


'''
定义一个方法，处理用户的管理员登录！
'''
def index(request):
    tp = loader.get_template("backend/index.html")
    html = tp.render({"count": 1, "vms": 2})
    return HttpResponse(html)


'''
定义一个方法，处理用户退出登录！
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


def listvm(request):
    if request.session.get('user_id'):
        try:
            # 连接vcenter服务器
            service_instance = connect.SmartConnectNoSSL(host="172.16.3.141",
                                                         user="administrator@vsphere.local",
                                                         pwd="Server@2012",
                                                         port=443)

            # 从根目录下查找虚拟机
            atexit.register(connect.Disconnect, service_instance)
            content = service_instance.RetrieveContent()
            container = content.rootFolder  # 从哪查找
            viewType = [vim.VirtualMachine]  # 查找的对象类型是什么
            recursive = True  # 是否进行递归查找
            containerView = content.viewManager.CreateContainerView(container, viewType, recursive)
            children = containerView.view  # 执行查找

            # 载入模板，传递一个集合给模板，让模板渲染成html返回
            tp = loader.get_template("backend/list.html")
            html = tp.render({"count": len(children), "vms": children})
            return HttpResponse(html)
        except vmodl.MethodFault as error:
            return HttpResponse("Caught vmodl fault : " + error.msg)
    else:
        tp = loader.get_template("backend/list.html")
        html = tp.render()
        return HttpResponse("页面未找到！")