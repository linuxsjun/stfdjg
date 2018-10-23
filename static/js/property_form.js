$(document).ready(function () {
    //----页面初始化----
    if ($('#act').val() === "create") {
        $('[data-dis="display"]').addClass("sr-only");
        $('[data-dis="edit"]').removeClass("sr-only");

        // $('button[data-toggle="save"]').removeClass("disabled");

        $('[data-toggle="tooltip"]').tooltip();
    }else {
        $('[data-dis="display"]').removeClass("sr-only");
        $('[data-dis="edit"]').addClass("sr-only");

        $('.form-control').attr('readonly', true);
        $('.custom-select').attr('disabled', true);
    }

    //----bars----
    $('#cateid').click(function () {
            $('#myModal').modal("show");
    });
    // ----管理工具条----
    $('button[data-toggle="edit"]').on('click', function () {
        if ($(this).hasClass('disabled')) {

        } else {
            $('[data-dis="display"]').addClass("sr-only");
            $('[data-dis="edit"]').removeClass("sr-only");

            $('.form-control').removeAttr('readonly', true);
            $('.custom-select').removeAttr('disabled', true);
            $('[data-toggle="tooltip"]').tooltip('enable');
            $('button[data-toggle="save"]').removeClass("disabled");

            $('#act').val('edit')
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
            // $('.form-control').attr('readonly', true);
            // $('.custom-select').attr('disabled', true);
            // $('[data-toggle="tooltip"]').tooltip('disable');
            // $('button[data-toggle="save"]').addClass("disabled");
            $.post(
                "/property_form/",
                $('form').serialize(),
                function(context,status){
                    window.location.href="/property_form?act=display&id="+context;
                }
            );
        }
    });

    $('button[data-toggle="goback"]').on('click', function () {
        if ($(this).hasClass('disabled')) {

        } else {
            // $('.form-control, .custom-select').attr('readonly', true);
            // $('button[data-toggle="save"]').addClass("disabled");
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
                $('ol[class="carousel-indicators"]').empty();
                $('div.carousel-inner').empty();
                $.each(data['data'],function (i,n) {
                    $('ol[class="carousel-indicators"]').append('<li data-target="#carouselExampleIndicators" data-slide-to="'+ i + '"></li>');
                    $('div[class="carousel-inner"]').append('<div class="carousel-item"><img class="d-block w-100 img-responsive" src="'+ n['filepath'] +'" data-src="holder.js/400x520" alt="Third slide"></div>')
                });
                $('li[data-target="#carouselExampleIndicators"]').first().addClass('active');
                $('div.carousel-item').first().addClass('active');

            }
        });
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
            success: function(context) {
                //请求成功时处理
                $('#headerimg').attr("src",context['filepath']);
                $('#headerimg').attr("data-id",context['id']);
            }
        });
    });


    $('#delimg').click(function () {
        var pid = $("#assetid").text();
        var id = $('#headerimg').attr('data-id');
        $.post(
            "/property_form/",
           {'act':'delimg', 'id':id, 'pid':pid},
            function (context,status) {
                // 根据返回值处理 1.失败 2.成功：无图、有图
                if (context['code'] == 0) {
                    $('#headerimg').attr("src",context['filepath']);
                    $('#headerimg').attr("data-id",context['id']);
                }
                if (context['code'] == 1){
                    alert('删除错误');
                }
                if (context['code'] == 2){
                    $('#headerimg').attr("src","holder.js/100x100");
                    $('#headerimg').attr("data-id",context['id']);
                }
            }
        );
    });
    
    // ----编辑模式----
    $('#sid').change(function () {
        // if $('#sid').val() == 1{
        //
        // }
        $('#siddis').text($('#sid').val());
    });

    // ---- 表单验证 ----
    // 转大写
    $('#sid').keyup(function () {
        $(this).val($(this).val().toUpperCase());
    });

    // --- name必填 ---
    $('#name').blur(function () {
        if($(this).val() == "") {
            $(this).addClass('is-invalid');
            $('button[data-toggle="save"]').addClass("disabled");
        }else{
            $(this).removeClass('is-invalid');
            $('button[data-toggle="save"]').removeClass("disabled");
        }
    });

    // sid 必填、不重复
    $('#sid').blur(function () {
        if($(this).val() == "") {
            $(this).addClass('is-invalid');
            $('button[data-toggle="save"]').addClass("disabled");
        }else{
             $.get(
                 "/property_form",
                 {act:'chacksid',sid:$(this).val()},
                 function (data) {
                     if (data.code == "0") {
                         $('button[data-toggle="save"]').removeClass("disabled");
                         $('#sid').removeClass('is-invalid');
                     } else {
                         $('button[data-toggle="save"]').addClass("disabled");
                         $('#sid').addClass('is-invalid');
                     }
                 });
        }
    });

    // sn 必填、不重复、改o为0
    // Todo 查询时不验证，修改时当前记录不与本记录重复
    $('#sn').blur(function () {
        // if($(this).att('readonly') != True) {
            if ($(this).val() == "") {
                $(this).addClass('is-invalid');
                $('button[data-toggle="save"]').addClass("disabled");
            } else {
                $.get(
                    "/property_form",
                    {act: 'chacksn', sn: $(this).val()},
                    function (data) {
                        if (data.code == "0") {
                            $('button[data-toggle="save"]').removeClass("disabled");
                            $('#sn').removeClass('is-invalid');
                        } else {
                            $('button[data-toggle="save"]').addClass("disabled");
                            $('#sn').addClass('is-invalid');
                        }
                    });
            }
        // }
    });

    $('#categoryid').change(function () {
        //Todo 同时修改配件的继承性
        if($(this).val() == 0) {
            $(this).addClass('is-invalid');
            $('button[data-toggle="save"]').addClass("disabled");
        }else{
            $(this).removeClass('is-invalid');
            $('button[data-toggle="save"]').removeClass("disabled");
        }
    });

    $('#user').change(function () {
        if($(this).val() == 0) {
            // $(this).addClass('is-invalid');
            // $('button[data-toggle="save"]').addClass("disabled");
        }else{
            $.get(
                '/property_form/',
                {act:'dishrinfo', hrid:$(this).val()},
                function(data) {
                    if(data.code == 0){
                        $("#department").html(data.data.departmentid__name);
                        $("#hrposition").html(data.data.employeeid__position);
                    } else{
                        $("#department").html("");
                        $("#hrposition").html("");
                    }
                }
            );
            // $(this).removeClass('is-invalid');
            // $('button[data-toggle="save"]').removeClass("disabled");
        }
    });
});