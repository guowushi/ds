# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# 引用VMware相关库
import atexit

import simplejson
# 从django.http命名空间引入一个HttpResponse的类
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from pyVim import connect
from pyVmomi import vim
from pyVmomi import vmodl
from vmm.model.models import vm_obj

# 引入我们创建的表单类
from vmm.model.forms import vm_regist
# 引用模型和表单
from vmm.model.models import users
from vmm.model.models import vms
from vmm.back import creat
from vmm.model.forms import user_regist
from vmm.back import config

'''
定义一个方法，处理用户的管理员登录！
'''


def index(request):
    if request.session.get('user_id'):
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
        j = 0
        i = 0
        for vm in vms_list:
            if (vm.summary.runtime.powerState == "poweredOn"):
                i += 1
            if not vm.config.template:
                j += 1
        tp = loader.get_template("backend/index.html")
        html = tp.render({"running": i, "vms": j})
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
            vm_infor = vms.objects.all()  # 获得vms表单信息
            user_info = users.objects.all()  # 获得users表单信息
            vms_include = []  # 用于打包虚拟机列表及其使用者
            for vm_sq in vm_infor:
                vms_obj = vm_obj()
                vms_obj.vm_ob = vm_sq
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


# -----------------------------------------------------------------------------------------------



'''
(2)创建虚拟机
'''


def createvm(request):
    if request.session.get('user_id'):
        if request.method == 'POST':  # 当提交表单时
            vm_regist_info = vm_regist(request.POST)  # form 包含提交的数据
            if vm_regist_info.is_valid():  # 如果提交的数据合法

                input_name = vm_regist_info.cleaned_data["vm_name"]
                db_vm_name = vms.objects.filter(vm_name=input_name)
                if (db_vm_name) & db_vm_name.values_list("vm_enabled") == 1:
                    return HttpResponse("该名称已存在")
                else:
                    if creat(vm_regist_info)&config(vm_regist_info):
                        a_vm_user_id = request.session.get('user_id')
                        a_vm_name =vm_regist_info.cleaned_data["vm_name"]
                        a_vm_purpose = vm_regist_info.cleaned_data["vm_purpose"]
                        a_vm_os = vm_regist_info.cleaned_data["vm_os"]
                        a_vm_cpu = vm_regist_info.cleaned_data["vm_cpu"]
                        a_vm_disk = vm_regist_info.cleaned_data["vm_disks"]
                        a_vm_type = vm_regist_info.cleaned_data["vm_type"]
                        a_vm_memory = vm_regist_info.cleaned_data["vm_memory"]
                        vms.objects.create(vm_user_id=a_vm_user_id,vm_name=a_vm_name,vm_purpose=a_vm_purpose,
                                           vm_os=a_vm_os,vm_cpu=a_vm_cpu,vm_disks=a_vm_disk,vm_memory =a_vm_memory,vm_os_admin=1,vm_type=a_vm_type)
                        return HttpResponse("创建成功, 请返回虚拟机列表页面查看")
                    else:
                        return HttpResponse("创建失败")
            else:
                return HttpResponse("输入错误")
        else:  # 当正常访问时
            vm_regist_info = vm_regist()
        return render(request, 'backend/createvm.html', {'form': vm_regist_info})
    else:
        return HttpResponse("你还未登录，点击<a href=\"/login/\">这里</a>登录!")




#--------------------------------------------------------------------------------------------
def dispapp(request):
    if request.session.get('user_id'):
        vm_infor = vms.objects.all()  # 获得vms表单信息
        user_infor=users.objects.all()
        vms_include = []  # 用于打包虚拟机列表及其使用者
        for vm_sq in vm_infor:
            if(vm_sq.vm_dispose==False):
                vms_obj = vm_obj()
                vms_obj.vm_ob = vm_sq
                for user in user_infor:
                    if (user.user_id == vm_sq.vm_user_id):
                        vms_obj.user = user.real_name
                        vms_obj.enabled = vm_sq.vm_enabled
                        break
                vms_include.append(vms_obj)
        tp = loader.get_template("backend/disapp.html")
        html = tp.render({ "vms": vms_include})
        return HttpResponse(html)
    else:
        return HttpResponse("页面未找到")


# -----------------------------------------------------------------------------------------------



'''
虚拟机电源管理
'''


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
    input_id = uuid
    db_info_renew = users.objects.get(vm_uuid=input_id)
    if op_type == '0':  # 关机
        action.ShutdownGuest()
        db_info_renew.vm_power = 0
        db_info_renew.save()
    elif op_type == '1':  # 开机
        action.PowerOn()
        db_info_renew.vm_power = 1
        db_info_renew.save()
    elif op_type == '-1':  # 重启
        action.RebootGuest()
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False), content_type="application/json")


# ---------------------------------------------------------------------------------------------------



'''
显示用户列表
'''


def profile(request):
    vm_infor = vms.objects.all()  # 获得vms表单信息
    user_info = users.objects.all()  # 获得users表单信息
    users_ob = []  # 存放信息列表
    for user in user_info:
        if user.user_password != "":
            user_ob = vm_obj()
            user_ob.user = user
            vms_ob = []
            for vm in vm_infor:
                if (vm.vm_user_id == user.user_id):
                    vms_ob.append(vm)
            user_ob.vm_list = vms_ob
            users_ob.append(user_ob)
    tp = loader.get_template("backend/profile.html")
    html = tp.render({"users": users_ob})
    return HttpResponse(html)


# --------------------------------------------------------------------------------------------------------




# 修改个人信息
def modify(request):
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
        tp = loader.get_template("backend/modify.html")
        html = tp.render()
        return HttpResponse(html)
