$(document).ready(function () {
    //----页面初始化----
    $('.form-control, .custom-select').attr('readonly', true);



    //----bars----
    // $('#cateid').on('click', function () {
    $('#cateid').click(function () {
            $('#myModal').modal("show");
    });
    // ----管理工具条----
    $('button[data-toggle="edit"]').on('click', function () {
        if ($(this).hasClass('disabled')) {

        } else {
            $('.form-control, .custom-select').removeAttr('readonly', true);
            $('button[data-toggle="save"]').removeClass("disabled");
        }
    });

    $('button[data-toggle="create"]').on('click', function () {
        if ($(this).hasClass('disabled')) {

        } else {
            alert("create");
        }
    });

    $('button[data-toggle="del"]').click(function () {
        if ($(this).hasClass('disabled')) {

        } else {
            $('#Md_del').modal("show");
        }
    });

    $('button[data-toggle="surdel"]').click(function () {
        $('#Md_del').modal('hide');
        var asid = $("#assetid").text();

        $.ajax({
            url:"/property_form/",
            type:"POST",
            data:{
                "act":"unactive",
                "id":asid
            },
            success:function (data) {
                window.location.href="/property_list/";
            },
            fail:function(){
                alert('删除失败!')
            }
        });

    });

    // ----编辑工具条----
    $('button[data-toggle="save"]').on('click', function () {
        if ($(this).hasClass('disabled')) {

        } else {
            alert("提交中,请等待...");
            $('.form-control, .custom-select').attr('readonly', true);
            $('button[data-toggle="save"]').addClass("disabled");
        }
    });

    $('button[data-toggle="goback"]').on('click', function () {
        if ($(this).hasClass('disabled')) {

        } else {
            $('.form-control, .custom-select').attr('readonly', true);
            $('button[data-toggle="save"]').addClass("disabled");
            window.location.href = "/property_list/";
        }
    });

    // ----扩展工具条----
    $('button[data-toggle="active"]').click(function () {
        var sel = $('button[data-toggle="active"]');
        var val = sel.attr("data-val");
        var asid = $("#assetid").text();
        var act = "";

        if (val == "1") {
            sel.attr("data-val",0);
            sel.html('<i class="fa fa-archive fa-1x"></i>取档');
            act = "unactive";
        }else {
            sel.attr("data-val", 1);
            sel.html('<i class="fa fa-archive fa-1x"></i>归档');
            act = "active";
        }
        $.ajax({
            url:"/property_form/",
            type:"POST",
            data:{
                "act":act,
                "id":asid
            },
            success:function (data) {

            }
        })
    });

    // ----头像----
    $('')
});
