# -*- coding: utf-8 -*-
from django.http import HttpResponse

# 导入vSphere SDK模块
import atexit
from pyVmomi import vim
from pyVim import connect
from vmm.models import vm_info


# 虚拟机电源管理
def vmpower(request):
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
    if op_type == '0':  # 关机
        action.ShutdownGuest()
    elif op_type == '1':  # 开机
        action.PowerOn()
    elif op_type == '-1':  # 重启
        action.RebootGuest()
    return HttpResponse(op_type)


# 修改信息
def modify():
    pass




# 申请虚拟机
def applyvm():
    pass




#创建虚拟机
def creatvm():
    pass





