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
from django.conf.urls import url
from django.contrib import admin
# 导入vmm.vmtest文件
import vmm.login
import vmm.admin
import vmm.user
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^listvm/', vmm.login.listvm),
    # -------------------------------
    url(r'^login/', vmm.login.login),
    url(r'^backend\/index', vmm.admin.index),
    url(r'^backend\/logout', vmm.admin.logout),  # 退出
    # -------------------------------
    url(r'^front\/index', vmm.user.index),
    url(r'^front\/profile', vmm.user.profile),  # 修改个人基本信息


]
