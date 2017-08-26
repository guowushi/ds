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
import vmm.common

# 验证码模块开始#
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

# 验证码模块结束#

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^listvm/', vmm.login.listvm),
    url(r'^captcha/', include('captcha.urls')),  # 这是生成验证码的图片
    url(r'^refresh/$', vmm.login.captcha_refresh, name='captcha-refresh'),  # 刷新验证码
    url(r'^logout', vmm.login.logout),  # 退出
    url(r'^login/', vmm.login.login),
    # -------------------------------
    url(r'^backend/index', vmm.admin.index),
    url(r'^backend/list', vmm.admin.listvm),
    url(r'^backend/power', vmm.admin.power),
    url(r'^backend/createvm', vmm.common.createvm),
    url(r'^backend/profile', vmm.admin.users_infor),
    # -------------------------------
    url(r'^front/index', vmm.user.index),
    url(r'^front/list', vmm.user.listvm),
    url(r'^front/profile', vmm.user.profile),  # 修改个人基本信息
]
