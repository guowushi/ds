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
    // 验证用户名
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
        $('.dlfrom').submit();
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


