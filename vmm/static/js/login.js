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
