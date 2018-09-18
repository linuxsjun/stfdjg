$(document).ready(function () {
    $('[data-toggle="gettoken"]').on('click',function () {
        var $btn = $(this).button('loading')
        $.ajax({
            url:"/gettoken",
            type:"GET",
            data:{
                "act":'gettoken'
            },
            success:function (data) {
                console.log(data)
            }
        })
        $btn.button('reset')
    })
})