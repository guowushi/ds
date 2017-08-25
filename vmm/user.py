# -*- coding:utf-8 -*-
# 从django.http命名空间引入一个HttpResponse的类
from django.http import HttpResponse
from django.template import loader, Context
# 引用VMware相关库
import atexit
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import vmm.tools.cli as cli
from vmm.admin import vm_obj
# 引用模型和表单
from vmm.models import users
from vmm.models import vms
'''
定义一个方法，处理用户的HTTP请求，并给出HTTP回复
'''
def index(request):
    tp = loader.get_template("front/index.html")
    html = tp.render({"count": 1, "vms": 2})
    return HttpResponse(html)


'''
定义一个方法，处理用户的HTTP请求，并给出HTTP回复
'''


def profile(request):
    tp = loader.get_template("front/profile.html")
    html = tp.render({"count": 1, "vms": 2})
    return HttpResponse(html)


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
            vms_list = containerView.view  # 执行查找
            vm_infor = vms.objects.all() # 获得vms表单信息
            user_info = users.objects.all() # 获得users表单信息
            vms_include = []                      # 用于打包虚拟机列表及其使用者
            for vm_vc in vms_list:
                vms_obj = vm_obj()
                vms_obj.vm_ob = vm_vc
                for vm_sq in vm_infor:
                    if(vm_vc.summary.config.uuid==vm_sq.vm_uuid):  #遍历数据库找到对应虚拟机使用者
                        for user in user_info:
                            if(user.user_id==vm_sq.vm_user_id):
                                vms_obj.user=user.real_name
                                vms_obj.enabled=vm_sq.vm_enabled
                                break
                vms_include.append(vms_obj)
            # 载入模板，传递一个集合给模板，让模板渲染成html返回
            tp = loader.get_template("front/list.html")
            html = tp.render({"vms": vms_include})
            return HttpResponse(html)
        except vmodl.MethodFault as error:
            return HttpResponse("Caught vmodl fault : " + error.msg)
    else:
        tp = loader.get_template("front/list.html")
        html = tp.render()
        return HttpResponse("页面未找到！")