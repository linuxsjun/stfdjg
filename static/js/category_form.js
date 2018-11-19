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
        $('.form-check-input').attr('disabled', true);
        $('.custom-select').attr('disabled', true);
    }

    // ----管理工具条----
    $('button[data-toggle="edit"]').on('click', function () {
        if ($(this).hasClass('disabled')) {

        } else {
            $('[data-dis="display"]').addClass("sr-only");
            $('[data-dis="edit"]').removeClass("sr-only");

            $('.form-control').removeAttr('readonly', true);
            $('.form-check-input').removeAttr('disabled', true);
            $('.custom-select').removeAttr('disabled', true);

            $('[data-toggle="tooltip"]').tooltip('enable');

            $('button[data-toggle="save"]').removeClass("disabled");

            $('#act').val('edit')
        }
    });

    $('button[data-toggle="cancel"]').on('click', function () {
        if ($(this).hasClass('disabled')) {

        } else {
            window.location.reload()
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
        var asid = $("#itemid").text();

        $.ajax({
            url:"/category_form/",
            type:"POST",
            data:{
                "act":"unactive",
                "id":asid
            },
            success:function () {
                window.location.href="/category_list/";
            },
            fail:function(){
                alert('删除失败!')
            }
        });
    });

    // ----编辑工具条----
    $('button[data-toggle="save"]').click(function () {
        // Todo 保存之前要做表单验证
        if ($(this).hasClass('disabled')) {

        } else {
            // $('.form-control').attr('readonly', true);
            // $('.custom-select').attr('disabled', true);
            // $('[data-toggle="tooltip"]').tooltip('disable');
            // $('button[data-toggle="save"]').addClass("disabled");
            // console.log($('form').serializeArray());
            $.post(
                "/category_form/",
                $('form').serialize(),
                function(context){
                    window.location.reload()
                }
            );

        }
    });

    $('button[data-toggle="goback"]').on('click', function () {
        if ($(this).hasClass('disabled')) {

        } else {
            window.location.href = "/category_list/";
        }
    });

    // ----扩展工具条----
    $('button[data-toggle="active"]').click(function () {
        var sel = $('button[data-toggle="active"]');
        var val = sel.attr("data-val");
        var asid = $("#itemid").text();
        var act = "";

        if (val === "1") {
            sel.attr("data-val",0);
            sel.html('<i class="fa fa-archive fa-1x"></i> 取档');
            act = "unactive";
        }else {
            sel.attr("data-val", 1);
            sel.html('<i class="fa fa-archive fa-1x"></i> 归档');
            act = "active";
        }
        $.ajax({
            url:"/category_form/",
            type:"POST",
            data:{
                "act":act,
                "id":asid
            },
            success:function (data) {
            }
        })
    });

    $('#btnaplsub').click(function () {
        var itemid = $('#id').val();
        var app = this;
        app.addClass('text-danger');
        $.post('/category_form/',
            {
                act:"aplsub",
                id:itemid
            },
            function (data) {
                console.log(data);
                app.removeClass('fa-pulse');
            }
        )
    });

    // ----编辑模式----
    $('#parentid').change(function () {
        //Todo 同时修改配件的继承性
        var val = $(this).val();
        var chkbom = $('#bom');
        if(val === '0') {
            chkbom.prop("checked", false);
        }else{
            $.get(
                '/property_form/',
                {act:'discategory', categoryid:val},
                function(data) {
                    if(data.code === 0){
                        if( data.data['bom']){
                            chkbom.prop("checked", true);
                        }else {
                            chkbom.prop("checked", false);
                        }
                    }else{
                    }
                }
            );
        }
    });
});