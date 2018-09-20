$(document).ready(function () {
    $('[data-toggle="gethr"]').on('click',function () {
        var $btn = $(this).button('loading')
        $.ajax({
            url:"/gethr",
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