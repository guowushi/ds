# -*- coding：utf-8 -*-
# 存放虚拟机对象和使用者禁用状态
class vm_obj(object):
    def __int__(self, vm_ob, user, enabled, vm_list):
        self.vm_ob = vm_ob
        self.user = user
        self.enabled = enabled
        self.vm_list = vm_list
