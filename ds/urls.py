# -*- coding:utf-8 -*-
"""ds URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
# 导入vmm.vmtest文件
import vmm.login
import vmm.admin
import vmm.user

# 验证码模块开始#
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

# 验证码模块结束#

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^captcha/', include('captcha.urls')),  # 这是生成验证码的图片
    url(r'^refresh/$', vmm.login.captcha_refresh, name='captcha-refresh'),  # 刷新验证码
    url(r'^logout', vmm.login.logout),  # 退出
    url(r'^login/', vmm.login.login),
    url(r'^backend/power', vmm.admin.power),  # 电源管理
    url(r'^userregist', vmm.login.userregist),  # 注册账号
    url(r'^active_user/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', vmm.login.active_user, name='active_user'),#邮件链接

    # -------------------------------
    url(r'^backend/index', vmm.admin.index),  # 首页
    url(r'^backend/list', vmm.admin.listvm),  # 虚拟机列表
    url(r'^backend/createvm', vmm.admin.createvm),  # 创建虚拟机
    url(r'^backend/dispapp', vmm.admin.dispapp),  # 待处理申请
    url(r'^backend/profile', vmm.admin.profile),  # 用户列表
    url(r'^backend/modify', vmm.admin.modify),  # 修改个人信息




    # -------------------------------
    url(r'^front/index', vmm.user.index),  # 首页
    url(r'^front/list', vmm.user.listvm),  #虚拟机列表
    url(r'^front/createvm', vmm.user.createvm),  # 申请虚拟机
    url(r'^front/modify', vmm.user.modify),  # 修改个人基本信息
    url(r'^dispose_vm/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', vmm.login.active_user, name='dispose_vm'),#邮件链接




]
