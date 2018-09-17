$(document).ready(function () {
    $('[data-toggle="gettoken"]').click(function () {
        $.ajax({
            url:"/gettoken/",
            type:"GET",
            data:{
                "act":'gettoken'
            },
            success:function (data) {
                alert(data)
            }
        })
    })
})