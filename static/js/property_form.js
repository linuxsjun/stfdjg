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
    $('#headerimg').click(function () {
        var asid = $("#assetid").text();
        //----请求照片表----
        $.ajax({
            url: "/property_form/",
            type: "GET",
            data: {
                "act": 'disheadimg',
                "id": asid
            },
            success: function (data) {
                $.each(data,function (i,n) {
                    $('ol[class="carousel-indicators"]').append('<li data-target="#carouselExampleIndicators" data-slide-to="'+ i + '"></li>');
                    $('div[class="carousel-inner"]').append('<div class="carousel-item"><img class="d-block w-100" src="'+ n['filepath'] +'" data-src="holder.js/400x520" alt="Third slide"></div>')
                });
                // $('li[data-target="#carouselExampleIndicators"]').first().addClass('active');
                // $('li[data-target="#carouselExampleIndicators"]').first().remove();
                // $('div[class="carousel-item active"]').first().addClass('active');
                // $('div.carousel-item').first().remove();
            }
        });

        //--有-无--
           //----插入照片表----

           //----空表
        $('#imglist').modal("show");
    });

     // ----头像上传----
    $('#upload').click(function () {
        return $('#imgupload').click();
    });

    $('#imgupload').change(function () {
        // alert($('#headerimgform')[0]);

        $.ajax({
            url:"/property_upload/",
            type:"post",
            cache: false,
            async:true,
            data:new FormData($('#headerimgform')[0]),
            processData: false,
            contentType: false,
            success: function(req) {
                //请求成功时处理
                $('#headerimg img').attr("src",req)
            }
        });
    });


    // $('#imgupload').fileupload(function () {
    //     // alert($('#imgupload').val());
    //
    // });
});
