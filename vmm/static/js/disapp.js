/**
 * Created by FuJinsong on 2017/8/25.
 */
$(document).ready(function(){

/*电源管理函数*/
    function power(optype,id) {
        var info = '';
        switch (optype){
            case -1:
                info = "拒绝";
                break;
            case 1:
                info = "同意";
                break;
        }
        bootbox.confirm("确定要" + info + "吗？", function (result) {
            if(result){
                $.ajax({
                    type: "POST",
                    url: "/backend/dispapp?id=" + id + "&type=" + optype,
                    success: function (msg) {
                    }

                });
            }

        })
    }

    $(".opt").on("click","button",function(){

        var id = $(this).parents('tr').find('input[name="checkbox"]').attr("value");
        var optype = '';
             // alert(id);
        if ($(this).attr('class').indexOf('btn_agree') != -1) {
            optype = 1;
            power(optype, id);
        } else if ($(this).attr('class').indexOf('btn_disagree') != -1) {
            optype = -1;
            power(optype, id);
        }
    });
});