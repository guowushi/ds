# -*- coding:utf-8 -*-
from django import forms
from captcha.fields import CaptchaField


class user_login(forms.Form):
    user_id = forms.CharField()
    user_password = forms.CharField()
    captcha = CaptchaField()  # 为生成的验 证码图片，以及输入框



class user_regist(forms.Form):
    user_id = forms.CharField()
    user_password1 = forms.CharField()
    user_password2 = forms.CharField()
    real_name = forms.CharField()
    email = forms.EmailField()


class vm_regist(forms.Form):
    vm_name = forms.CharField()
    vm_password = forms.CharField()
    vm_os = forms.CharField()
    vm_cpu = forms.IntegerField()
    vm_memory = forms.IntegerField()
    vm_disk = forms.IntegerField()
    vm_purpose = forms.CharField()
