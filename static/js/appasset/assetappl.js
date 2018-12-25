$(function () {
    //领用、借用切换
    $("[name='type']").change(function () {
        var typen = $(this).val();
        console.log(typen);
        $("#borrowdate").toggleClass("sr-only")
    });

    // 事由必填
    $("#explain").blur(function () {
        var me=$("#explain");
        var btn_submit=$('#submit');

        if (me.val() === null) {
            btn_submit.addClass('disabled')
        } else {
            btn_submit.removeClass('disabled')
        }
    });

    // todo 设备选择必填
    $("#explain").blur(function () {
        var me=$("#explain");
        var btn_submit=$('#submit');

        if (me.val() === null) {
            btn_submit.addClass('disabled')
        } else {
            btn_submit.removeClass('disabled')
        }
    });

    // 提交
    $("#submit").click(function () {
        if ($(this).hasClass('disabled')) {
        } else {
            $.post("/asset/assetappl/",
                $('form').serialize(),
                function (data) {
                });
        }
    });
});