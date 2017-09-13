# -*- coding: utf-8 -*-
# 导入vSphere SDK模块
import atexit

from django.http import HttpResponse
from django.template import loader
from pyVim import connect
from pyVim.connect import Disconnect
from pyVmomi import vim
from vmm.model.models import vms
from vmm.model.token import Token
from vmm.model.forms import vm_regist
from django.conf import settings
from vmm.model.models import users
#-------------------------------------------------------------------------------------------------
# 创建虚拟机
def wait_for_task(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            print("there was an error")
            task_done = True


def get_obj(content, vimtype, name):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    return obj


def clone_vm(
        content, template, vm_name, si,
        datacenter_name, vm_folder, datastore_name,
        cluster_name, resource_pool, power_on):
    """
    Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
    cluster_name, resource_pool, and power_on are all optional.
    """
    # if none git the first one
    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)

    if vm_folder:
        destfolder = get_obj(content, [vim.Folder], vm_folder)
    else:
        destfolder = datacenter.vmFolder

    if datastore_name:
        datastore = get_obj(content, [vim.Datastore], datastore_name)
    else:
        datastore = get_obj(
            content, [vim.Datastore], template.datastore[0].info.name)

    # if None, get the first one
    cluster = get_obj(content, [vim.ClusterComputeResource], cluster_name)

    if resource_pool:
        resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)
    else:
        resource_pool = cluster.resourcePool

    # set relospec
    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = resource_pool

    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.powerOn = power_on
    task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
    wait_for_task(task)


def creat(vm_regist_info):
    os=vm_regist_info.cleaned_data["vm_os"]
    name=vm_regist_info.cleaned_data["vm_name"]
    """
    Let this thing fly
    """
    # connect this thing
    si = connect.SmartConnectNoSSL(
        host="172.16.3.141",
        user="administrator@vsphere.local",
        pwd="Server@2012",
        port=443)
    # disconnect this thing
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    container = content.rootFolder  # 从哪查找
    viewType = [vim.VirtualMachine]  # 查找的对象类型是什么
    recursive = True  # 是否进行递归查找
    containerView = content.viewManager.CreateContainerView(container, viewType, recursive)
    vms_list = containerView.view  # 执行查找
    # db_info_renew = vms.objects.get(user_id=input_id)



    content = si.RetrieveContent()
    template = None

    template = get_obj(content, [vim.VirtualMachine], os)

    if template:
        clone_vm(
            content, template,name , si,
            "Datacenter", "auto_regist",
            "", "Server3,4,5",
            "test", 0)

        return True
    else:
        return False




#------------------------------------------------------------------------------------------------------------



#修改虚拟机配置
def config(vm_regist_info):
    """
    Let this thing fly
    """
    # connect this thing
    name = vm_regist_info.cleaned_data["vm_name"]
    CPU = vm_regist_info.cleaned_data["vm_cpu"]
    memory = vm_regist_info.cleaned_data["vm_memory"]
    si = connect.SmartConnectNoSSL(
        host="172.16.3.141",
        user="administrator@vsphere.local",
        pwd="Server@2012",
        port=443)
    # disconnect this thing
    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    container = content.rootFolder
    viewType = [vim.VirtualMachine]
    recursive = True
    containerView = content.viewManager.CreateContainerView(
        container, viewType, recursive)
    children = containerView.view
    for vm in children:
        if vm.name == name:
            numCPUs = vim.vm.ConfigSpec()
            numCPUs.numCPUs = CPU
            numCPUs.numCoresPerSocket = CPU / 2
            numCPUs.memoryMB = memory
            vm.ReconfigVM_Task(numCPUs)
            return True
    return False



token_confirm = Token(settings.SECRET_KEY)

#申请处理页面
def dispose_vm(request, token):

    try:
        vm_name = token_confirm.confirm_validate_token(token)
    except:
        return HttpResponse(u'对不起，验证链接已经过期')
    try:
        vm = vms.objects.get(vm_name=vm_name)
    except users.DoesNotExist:
        return HttpResponse(u'对不起，您所验证的用户不存在，请重新注册')
    vm.vm_dispose = True
    vm.vm_enabled=1
    vm.save()
    tp = loader.get_template("re_success.html")
    html = tp.render()
    return HttpResponse(html)