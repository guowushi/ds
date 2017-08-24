# vmcloud
this is cloud managment system base on vmware  Vcenter
功能
（1）申请虚拟机
用户可以自我申请虚拟机，虚拟机支持两种模板（Linux和Windows）。可以自行选择CPU和内存，填写“业务说明”、“备注”、“开放端口”、选择“虚拟机类型”。
虚拟机名称会自动产生。具体规则：
模板名+IP+用户ID。例如“win7-192.168.1.1-zhangsan”
（2）虚拟机电源管理
用户可以在后台对自己所拥有的虚拟机进行电源管理（关闭、启动）。
（3）虚拟机异常报警
虚拟机在掉电、启动事件发生时，则会通过邮件通知拥有者和系统管理员。

系统架构
开发语言：python
Web框架：Django
前段框架：http://zui.sexy/


\static存放第三方的静态资源，如Jquery，zui。不要放自己的静态资源
vmm 管理系统的模块
 属于vmm模块的静态资源放在vmm\static\下
 属于vmm模块的模板放在vmm\templates\下  backend放管理员相关的，front放普通用户相关的

管理用户视图
    admin.py
普通用户视图
    user.py

通用视图
    登录视图
        login.py
    通用功能视图
        common.py






