# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# 从django.http命名空间引入一个HttpResponse的类
from django.http import HttpResponse
from django.template import loader, Context
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
import simplejson

# 引用VMware相关库
import atexit
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim

# 引用模型和表单
from vmm.models import users
from vmm.models import vms
# 引入我们创建的表单类
from vmm.forms import vm_regist

'''
定义一个方法，处理用户的管理员登录！
'''


def index(request):
    if request.session.get('user_id'):
        tp = loader.get_template("backend/index.html")
        html = tp.render({"count": 1, "vms": 2})
        return HttpResponse(html)
    else:
        return HttpResponse("error!")


# ---------------------------------------------------------------------------------------------------------------

'''
（1）显示所有的虚拟机列表
'''


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
            vm_infor = vms.objects.all()  # 获得vms表单信息
            user_info = users.objects.all()  # 获得users表单信息
            vms_include = []  # 用于打包虚拟机列表及其使用者
            for vm_vc in vms_list:
                vms_obj = vm_obj()
                vms_obj.vm_ob = vm_vc
                for vm_sq in vm_infor:
                    if (vm_vc.summary.config.uuid == vm_sq.vm_uuid):  # 遍历数据库找到对应虚拟机使用者
                        for user in user_info:
                            if (user.user_id == vm_sq.vm_user_id):
                                vms_obj.user = user.real_name
                                vms_obj.enabled = vm_sq.vm_enabled
                                break
                vms_include.append(vms_obj)
            # 载入模板，传递一个集合给模板，让模板渲染成html返回
            tp = loader.get_template("backend/list.html")
            html = tp.render({"vms": vms_include})
            return HttpResponse(html)
        except vmodl.MethodFault as error:
            return HttpResponse("Caught vmodl fault : " + error.msg)
    else:
        tp = loader.get_template("backend/list.html")
        html = tp.render()
        return HttpResponse("页面未找到！")


'''
(2)创建虚拟机
'''


def createvm(request):
    user_number = request.session.get('user_number')
    if request.session.get('user_number'):
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
        return render(request, 'backend/createvm.html', {'form': vm_regist_info})
    else:
        return HttpResponse("你还未登录，点击<a href=\"/login/\">这里</a>登录!")


def dispapp(request):
    tp = loader.get_template("backend/disapp.html")
    html = tp.render({"count": 1, "vms": 2})
    return HttpResponse(html)


class vm_obj(object):
    def __int__(self, vm_ob, user, enabled, vm_list):
        self.vm_ob = vm_ob
        self.user = user
        self.enabled = enabled
        self.vm_list = vm_list


# 虚拟机电源管理
def power(request):
    uuid = request.GET.get('uuid')
    op_type = request.GET.get('type')
    print (op_type)
    try:
        si = connect.SmartConnectNoSSL(host="172.16.3.141",
                                       user="administrator@vsphere.local",
                                       pwd="Server@2012",
                                       port=443)
    except vim.fault.InvalidLogin:
        print("Could not connect to the specified host using specified "
              "username and password")
        return -1

    atexit.register(connect.Disconnect, si)
    action = si.content.searchIndex.FindByUuid(None, uuid, True, True)
    data = {"type": op_type}
    if op_type == '0':  # 关机
        action.ShutdownGuest()
    elif op_type == '1':  # 开机
        action.PowerOn()
    elif op_type == '-1':  # 重启
        action.RebootGuest()
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False), content_type="application/json")


'''
显示用户信息
'''


def users_infor(request):
    vm_infor = vms.objects.all()  # 获得vms表单信息
    user_info = users.objects.all()  # 获得users表单信息
    users_ob = []  # 存放信息列表
    for user in user_info:
        user_ob = vm_obj()
        user_ob.user = user
        vms_ob = []
        for vm in vm_infor:
            if (vm.vm_user_id == user.user_id):
                vms_ob.append(vm)
        user_ob.vm_list = vms_ob
        users_ob.append(user_ob)

    print (users_ob[1].user.real_name)
    tp = loader.get_template("backend/profile.html")
    html = tp.render({"users": users_ob})
    return HttpResponse(html)


'''
显示用户信息
'''


def users_infor(request):
    vm_infor = vms.objects.all()  # 获得vms表单信息
    user_info = users.objects.all()  # 获得users表单信息
    users_ob = []  # 存放信息列表
    for user in user_info:
        user_ob = vm_obj()
        user_ob.user = user
        vms_ob = []
        for vm in vm_infor:
            if (vm.vm_user_id == user.user_id):
                vms_ob.append(vm)
        user_ob.vm_list = vms_ob
        users_ob.append(user_ob)

    print (users_ob[1].user.real_name)
    tp = loader.get_template("backend/profile.html")
    html = tp.render({"users": users_ob})
    return HttpResponse(html)


def modify(request):
    pass
