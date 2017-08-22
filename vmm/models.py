# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


# 创建用户信息表
class users(models.Model):
    real_name = models.CharField(max_length=20)
    user_id = models.CharField(max_length=20, primary_key=True)
    user_password = models.CharField(max_length=20)
    email = models.EmailField(max_length=40, primary_key=True)
    mobile = models.CharField(blank=True)
    isadmin = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    def __unicode__(self):  # 在Python3中使用 def __str__(self):
        return self.user_id  # 返回这张表的主键，用于区分数据库中的不同表


# 创建虚拟机信息表
class vms(models.Model):
    vm_name = models.CharField(max_length=50, primary_key=True)
    vm_uuid = models.CharField(max_length=50, primary_key=True)
    vm_purpose = models.TextField()
    vm_comment = models.TextField()
    vm_os_admin = models.CharField(max_length=20)
    vm_os_pass = models.CharField(blank=True)
    vm_owner = models.CharField(max_length=20)
    vm_type = models.IntegerField()
    vm_ports = models.CharField(max_length=20)

    vm_ip = models.CharField(max_length=15, db_index=True)
    vm_os = models.CharField(max_length=20)
    vm_cpu = models.IntegerField()
    vm_memory = models.IntegerField()
    vm_disks = models.IntegerField()
    vm_enabled = models.IntegerField(default=False)

    def __unicode__(self):
        return self.vm_uuid
