/**
 * Created by FuJinsong on 2017/8/25.
 */
$(document).ready(function(){

/*电源管理函数*/
    function power(optype,uuid) {
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

                    }
                });
            }

        })
    }

    $(".opt button").on("click",function(){
        var uuid = $(this).parents('tr').find('input[name="checkbox"]').attr("value");
        var optype = '';
        // alert(uuid);
        if ($(this).attr('class').indexOf('btn_poweroff') != -1) {
            optype = 0;
            power(optype, uuid);
        } else if ($(this).attr('class').indexOf('btn_reboot') != -1) {
            optype = -1;
            power(optype, uuid);
        } else if ($(this).attr('class').indexOf('btn_poweron') != -1) {
            optype = 1;
            power(optype, uuid);
        }
    });
});