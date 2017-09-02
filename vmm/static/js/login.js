/**
 * Created by FuJinsong on 2017/8/22.
 */

/*刷新验证码*/
$('.captcha').click(function () {
    console.log('click');
    $.getJSON("/captcha/refresh/",
        function (result) {
            $('.captcha').attr('src', result['image_url']);
            $('#id_captcha_0').val(result['key'])
        });
});

/*登录校验*/
var userok = false;
var passok = false;
var captchaok = false;
$('.denglu').click(function () {
    // 验证用户名密码和验证码是否为空！
    if ($('input[name="user_id"]').val() != "") {
        userok = true;
        if ($('input[name="user_password"]').val() != "") {
            passok = true;
            if ($('input[name="captcha_1"]').val() != "") {
                captchaok = true;
            }
            else {
                captchaok = false;
                $('input[name="captcha_1"]').parent('.col-md-6').addClass('has-warning');
                $('[data-toggle="captip"]').tooltip({
                    tipClass: 'tooltip-warning',
                    title: '验证码不能为空！',
                    placement: 'right'
                });
                $('input[name="captcha_1"]').tooltip('show');
            }
        }
        else {
            passok = false;
            $('input[name="user_password"]').parent('.col-md-6').addClass('has-warning');
            $('[data-toggle="passtip"]').tooltip({
                tipClass: 'tooltip-warning',
                title: '密码不能为空！',
                placement: 'right'
            });
            $('input[name="user_password"]').tooltip('show');
        }
    }
    else {
        userok = false;
        $('input[name="user_id"]').parent('.col-md-6').addClass('has-warning');
        $('[data-toggle="usertip"]').tooltip({
            tipClass: 'tooltip-warning',
            title: '用户名不能为空！',
            placement: 'right'
        });
        $('input[name="user_id"]').tooltip('show');
    }

    //提交按钮,所有验证通过方可提交
    if (userok && passok && captchaok) {
        // console.log(form);
        $(".dlfrom").ajaxSubmit({
            type: "POST",
            dataType: "json", //json格式，后台返回的数据为json格式的。
            success: function (result) {
                console.log(result);
                if (result.captcha == true) {
                    if (result.user_pass == false) {
                        new $.zui.Messager('用户名或密码错误。', {
                            type: 'warning',
                            icon: 'warning-sign',
                            time: '3000',
                            placement: 'center' // 定义显示位置
                        }).show();
                    }else if(result.admin == true){
                        window.location = "/backend/index";
                    }else{
                        window.location = "/front/index";
                    }
                } else {
                    new $.zui.Messager('验证码错误。', {
                        type: 'warning',
                        icon: 'warning-sign',
                        time: '3000',
                        placement: 'center' // 定义显示位置
                    }).show();
                }
            }
        });
    }

});
    $('input[name="user_id"]').click(function () {
        $(this).parent('.col-md-6').removeClass('has-warning');
        $(this).tooltip('destroy');
    });
    $('input[name="user_password"]').click(function () {
        $(this).parent('.col-md-6').removeClass('has-warning');
        $(this).tooltip('destroy');
    });
    $('input[name="captcha_1"]').click(function () {
        $(this).parent('.col-md-6').removeClass('has-warning');
        $(this).tooltip('destroy');
    });


    // 注册框验证是否为空
$('.reg_bt').click(function () {
    var input_id = $("#reg_bd input");
    for(var i=0;i<input_id.length;i++){
        if ($(input_id[i]).val() == "" && !($(input_id[i]).hasClass('norequired'))){
            // alert();
            var name = $(input_id[i]).parent().prev('label').text();
            var tip = $(input_id[i]).attr('data-toggle');
            $(input_id[i]).parent('.col-md-6').addClass('has-warning');
            $('[data-toggle='+ tip +']').tooltip({
                tipClass: 'tooltip-warning',
                title: name + '不能为空！',
                placement: 'right'
            });
            $(input_id[i]).tooltip('show');
            break;
        }
        else {
            $(".regform").ajaxSubmit({
                type: "POST",
                dataType: "json", //json格式，后台返回的数据为json格式的。
                success: function (result) {
                    console.log(result);
                    if(result.reg == "输入错误"){
                        new $.zui.Messager('输入错误字段。', {
                            type: 'warning',
                            icon: 'warning-sign',
                            time: '3000',
                            placement: 'center' // 定义显示位置
                        }).show();
                    }else if(result.reg == "该账号不能注册"){
                        new $.zui.Messager('请输入教师账号', {
                        type: 'warning',
                        icon: 'warning-sign',
                        time: '3000',
                        placement: 'center' // 定义显示位置
                    }).show();
                    }else if(result.reg == "已有密码"){
                        new $.zui.Messager('该账号已被注册', {
                        type: 'warning',
                        icon: 'warning-sign',
                        time: '3000',
                        placement: 'center' // 定义显示位置
                    }).show();
                    }else if(result.reg == "注册"){
                        new $.zui.Messager('请前往邮箱验证', {
                        type: 'warning',
                        icon: 'warning-sign',
                        time: '3000',
                        placement: 'center' // 定义显示位置
                    }).show();
                    }else if(result.reg == "密码不匹配"){
                        new $.zui.Messager('密码不匹配', {
                        type: 'warning',
                        icon: 'warning-sign',
                        time: '3000',
                        placement: 'center' // 定义显示位置
                    }).show();
                    }else if(result.reg == "页面"){
                        new $.zui.Messager('请前往登录页面注册', {
                        type: 'warning',
                        icon: 'warning-sign',
                        time: '3000',
                        placement: 'center' // 定义显示位置
                    }).show();
                    }


                }
            });
            break;

        }
    }
});

$('input[name="real_name"]').click(function () {
    $(this).parent('.col-md-6').removeClass('has-warning');
    $(this).tooltip('destroy');
});

$('input[name="user_password1"]').click(function () {
    $(this).parent('.col-md-6').removeClass('has-warning');
    $(this).tooltip('destroy');
});

$('input[name="user_password2"]').click(function () {
    $(this).parent('.col-md-6').removeClass('has-warning');
    $(this).tooltip('destroy');
});

// $('input[name="mobile"]').click(function () {
//     $(this).parent('.col-md-6').removeClass('has-warning');
//     $(this).tooltip('destroy');
// });

$('input[name="email"]').click(function () {
    $(this).parent('.col-md-6').removeClass('has-warning');
    $(this).tooltip('destroy');
});

//  $('input[name="comment"]').click(function () {
//     $(this).parent('.col-md-6').removeClass('has-warning');
//     $(this).tooltip('destroy');
// });




    // 找回密码框验证是否为空
$('.Fpass').click(function () {
    var input_id = $(".findp input");
    for(var i=0;i<input_id.length;i++){
        if ($(input_id[i]).val() == ""){
            // alert();
            var name = $(input_id[i]).prev('label').text();
            var tip = $(input_id[i]).attr('data-toggle');
            $(input_id[i]).parent('.col-md-6').addClass('has-warning');
            $('[data-toggle='+ tip +']').tooltip({
                tipClass: 'tooltip-warning',
                title: name + '不能为空！',
                placement: 'right'
            });
            $(input_id[i]).tooltip('show');
            break;
        }
        else{
            $(".regform").ajaxSubmit({
                type: "POST",
                dataType: "json", //json格式，后台返回的数据为json格式的。
                success: function (result) {
                    console.log(result);
                }
            });
        }
    }
});

$('input[name="f_id"]').click(function () {
    // $(this).parent('.col-md-6').removeClass('has-warning');
    $(this).tooltip('destroy');
});