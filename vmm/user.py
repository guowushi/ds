# -*- coding:utf-8 -*-
# 从django.http命名空间引入一个HttpResponse的类
# 引用VMware相关库
import atexit

from django.http import HttpResponse
from django.template import loader
from pyVim import connect
from pyVmomi import vim
from pyVmomi import vmodl

from vmm.admin import vm_obj
# 引用模型和表单
from vmm.model.models import vms

from vmm.model.forms import vm_regist
from django.shortcuts import render


'''
定义一个方法，处理用户的HTTP请求，并给出HTTP回复
'''
'''
主页
'''
def index(request):
    if request.session.get('user_id'):
        tp = loader.get_template("front/index.html")
        html = tp.render({"count": 1, "vms": 2})
        return HttpResponse(html)
    else:
        return HttpResponse("error!")


'''
定义一个方法，处理用户的HTTP请求，并给出HTTP回复
'''


def profile(request):
    tp = loader.get_template("front/profile.html")
    html = tp.render({"count": 1, "vms": 2})
    return HttpResponse(html)


def listvm(request):
    user_id = request.session.get('user_id')
    if user_id:
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
            vm_infor = vms.objects.all()  # 获得vms表单信息
            vms_include = []  # 用于打包虚拟机列表及其使用者
            for vm_sq in vm_infor:
                if (vm_sq.vm_user_id == user_id):
                    for vm_vc in vms_list:
                        if (vm_sq.vm_uuid == vm_vc.summary.config.uuid):
                            vms_obj = vm_obj()
                            vms_obj.vm_ob = vm_vc
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






'''
申请虚拟机
'''
def createvm(request):
    user_number = request.session.get('user_id')
    if request.session.get('user_id'):
        if request.method == 'POST':  # 当提交表单时
            vm_regist_info = vm_regist(request.POST)  # form 包含提交的数据
            if vm_regist_info.is_valid():  # 如果提交的数据合法
                print("输入数据合法！ ")
                print(vm_regist_info.cleaned_data)
            else:
                print("输入数据不合法！")
                print(vm_regist_info.cleaned_data)
        else:  # 当正常访问时
            vm_regist_info = vm_regist()
        return render(request, 'front/applicate.html', {'form': vm_regist_info})
    else:
        return HttpResponse("你还未登录，点击<a href=\"/login/\">这里</a>登录!")



'''
修改个人信息
'''
def modify(request):
    tp = loader.get_template("front/modify.html")
    html = tp.render()
    return HttpResponse(html)