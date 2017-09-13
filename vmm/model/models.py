# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


# 创建用户信息表
class users(models.Model):
    real_name = models.CharField(max_length=20)
    user_id = models.CharField(max_length=20, primary_key=True)
    user_password = models.CharField(max_length=20)
    email = models.EmailField(max_length=40)
    mobile = models.CharField(max_length=11,blank=True)
    isadmin = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    isactive=models.BooleanField(default=False)

    def __unicode__(self):  # 在Python3中使用 def __str__(self):
        return self.user_id  # 返回这张表的主键，用于区分数据库中的不同表


# 创建虚拟机信息表
class vms(models.Model):
    vm_name = models.CharField(max_length=50)
    vm_uuid = models.CharField(max_length=50, primary_key=True)
    vm_purpose = models.TextField()
    vm_comment = models.TextField()
    vm_os_admin = models.IntegerField()
    vm_os_password = models.CharField(max_length=20,blank=True)
    vm_user_id = models.CharField(max_length=20)
    vm_type = models.IntegerField()
    vm_ports = models.CharField(max_length=20)

    vm_ip = models.CharField(max_length=20)
    vm_os = models.CharField(max_length=20)
    vm_cpu = models.IntegerField()
    vm_memory = models.IntegerField()
    vm_disks = models.IntegerField()
    vm_enabled = models.IntegerField(default=1)
    vm_power = models.IntegerField(default=0)
    vm_dispose=models.BooleanField(default=False)
    def __unicode__(self):
        return self.vm_uuid



'''
自定义的类,用来存放相关数据
'''
class vm_obj(object):
    def __int__(self, vm_ob, user, enabled, vm_list):
        self.vm_ob = vm_ob
        self.user = user
        self.enabled = enabled
        self.vm_list = vm_list