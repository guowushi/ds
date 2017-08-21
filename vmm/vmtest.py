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


def hellovm(request):
    return HttpResponse("hello VM!")


'''
显示所有的虚拟机
'''


def listvm(request):
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
        tp = loader.get_template("myvmlist.html")
        html = tp.render({"count": len(children), "vms": children})
        return HttpResponse(html)
    except vmodl.MethodFault as error:
        return HttpResponse("Caught vmodl fault : " + error.msg)
