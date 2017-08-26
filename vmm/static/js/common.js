$(document).ready(function(){
    // els = $('.table > tbody > tr');for(ind=0;ind<els.length;ind++){$(els[ind]).attr('id','tr'+ind);}

    $('.sidebar .item.vertical > a').click(function () {
        var ver = jQuery(this).next();
        if (ver.is(":visible")) {
            jQuery(this).parent().removeClass("open");
            jQuery(this).parent().removeClass("active");
            ver.slideUp(200);
        } else {
            jQuery(this).parent().addClass("open");
            jQuery(this).parent().addClass("active");
            ver.slideDown(200);
        }
    });

    $(function () {
        function responsiveView() {
            var wSize = $(window).width();
            if (wSize <= 768) {
                $('.main').addClass('sidebar-close');
                $('.sidebar .sidebar-menu').hide();
            }

            if (wSize > 768) {
                $('.main').removeClass('sidebar-close');
                $('.sidebar .sidebar-menu').show();
            }
        }

        $(window).on('load', responsiveView);
        $(window).on('resize', responsiveView);
    });

    $('.sidebar-toggle').click(function () {
        if ($('.sidebar .sidebar-menu').is(":visible") === true) {
            $('.main-content').css({
                'margin-left': '0px'
            });
            $('.sidebar').css({
                'margin-left': '-180px'
            });
            $('.sidebar .sidebar-menu').hide();
            $(".main").addClass("sidebar-closed");
        } else {
            $('.main-content').css({
                'margin-left': '180px'
            });
            $('.sidebar .sidebar-menu').show();
            $('.sidebar').css({
                'margin-left': '0'
            });
            $(".main").removeClass("sidebar-closed");
        }
    });

    // 点击注销
    $('#logout').click(function () {
        bootbox.confirm("确定要退出", function () {
            $.post("/logout", function (data) {
                if (data.ok == 'true') {
                    window.location = "/login";
                }
            });
        })
    });

    // //切换页面的函数
    // function shiftpage(page) {
    //     if(page == 'index'){
    //         $('.panel').load('/backend/index #listvmm');
    //     }else if(page == 'list'){
    //         $('.panel').load('/backend/list #listvmm');
    //         // history.pushState({}, "页面标题", "xxx.html");
    //     }else if(page == 'apply'){
    //         $('.panel').load('/backend/list #listvmm');
    //     }else if(page == 'user'){
    //         $('.panel').load('/backend/list #listvmm');
    //     }else{
    //         return false;
    //     }
    // }
    //
    // $('#ad_main').click(function () {
    //     shiftpage('index');
    // });
    //
    // $('#ad_vm').click(function () {
    //     shiftpage('list');
    // });

});


