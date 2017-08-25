$(document).ready(function(){
    els = $('.table > tbody > tr');for(ind=0;ind<els.length;ind++){$(els[ind]).attr('id','tr'+ind);}

    $('.sidebar .item.vertical > a').click(function () {
        var ver = jQuery(this).next();
        if (ver.is(":visible")) {
            jQuery(this).parent().removeClass("open");
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

    //切换页面的函数
    function shiftpage(page) {
        if(page == 'index'){
            $('.panel').load('/backend/index #listvmm');
        }else if(page == 'list'){
            $('.panel').load('/backend/list #listvmm');
            // history.pushState({}, "页面标题", "xxx.html");
        }else if(page == 'apply'){
            $('.panel').load('/backend/list #listvmm');
        }else if(page == 'user'){
            $('.panel').load('/backend/list #listvmm');
        }else{
            return false;
        }
    }

    $('#ad_main').click(function () {
        shiftpage('index');
    });

    $('#ad_vm').click(function () {
        shiftpage('list');
        /*给表格的tr加上ID，方便识别具体行数*/
// -------------------------------------------------
        setTimeout("els = $('.table > tbody > tr');for(ind=0;ind<els.length;ind++){$(els[ind]).attr('id','tr'+ind);}",3000);
// -------------------------------------------------
    });

/*电源管理函数*/
    function power(optype,uuid,trid) {
        var info = '';
        switch (optype){
            case -1:
                info = "重启";
                break;
            case 0:
                info = "关机";
                break;
            case 1:
                info = "开机";
                break;
        }
        bootbox.confirm("确定要" + info + "吗？", function (result) {
            if(result){
                $.ajax({
                    type: "GET",
                    url: "/backend/power?uuid=" + uuid + "&type=" + optype,
                    success: function (msg) {
                        setTimeout(function () {
                            // var sss = $('#' + trid).children('.uuid').attr('value');
                            $('.panel-body').load('/backend/list table');
                        }, 15000);
                    }
                });
            }

        })
    }


    $('.panel').on("click","tr,td,button",function (event) {
        var tr_id = $(this).parents('tr').attr('id');
        var uu_id = $(this).nextAll('.uuid').attr('value');
        // console.log(123);
        // alert(uu_id);
        var optype = '';
        if ($(this).attr('id') == 'poweroff') {
            optype = 0;
            power(optype,uu_id,tr_id);
        }else if($(this).attr('id') == 'powerre'){
            optype = -1;
            power(optype,uu_id,tr_id);
        }else if($(this).attr('id') == 'poweron'){
            optype = 1;
            power(optype,uu_id,tr_id);
        }
        // return false;//阻止事件继续冒泡。
        event.stopPropagation();
    });

});


