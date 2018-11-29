$(document).ready(function () {
    // ----扩展函数----
    $.fn.extend({
        'selpartscategoryid':function (data) {
            var htxt = "";
            $.each(data,function (i,items) {
                htxt +='<option value=' + items['id'] + '>' + items['disn'] + ' (' + items['num'] + ')</option>';
            });
            return htxt;
        },
        'tabpartsadd':function (data) {
            var htxt = "";
            //     <tr>
            //     <td scope="col"><input type="checkbox" name="selitem" value="{{ item.id }}"></td>
            //     <td scope="col">电源</td>
            //     <td scope="col">山特 CASTLE 2K</td>
            //     <td scope="col">SANTAK UPS</td>
            //     <td scope="col">9103-7339-02P</td>
            //     <td scope="col"><i class="fa fa-exclamation-triangle fa-1x text-warning"></i></td>
            //      <td scope="col"><i class="fa fa-minus-square fa-1x text-danger"></i></td>
            //     <td scope="col"><i class="fa fa-check-square fa-1x text-success"></i></td>
            // </tr>
            $.each(data,function (i,items) {
                htxt +='<tr>';
                htxt +='<td scope="col"><input type="checkbox" name="selitem" value="' + items['id'] + '"></td>';
                htxt +='<td scope="col">' + items['name'] + '</td>';
                // htxt +='<td scope="col">' + items['model'] + '</td>';
                htxt +='<td scope="col">' + items['specifications'] + '</td>';
                htxt +='<td scope="col">' + items['sn'] + '</td>';
                // Todo 配件的状态用彩色图标来显示
                htxt +='<td scope="col">' + items['statusstr'] + '</td>';
                htxt +='</tr>';
            });
            return htxt;
        }
    });
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
            $('.form-check-input').removeAttr('disabled', true);
            $('.custom-select').removeAttr('disabled', true);
            $('[data-toggle="tooltip"]').tooltip('enable');
            $('button[data-toggle="save"]').removeClass("disabled");
            $('#addpart').removeClass("disabled");

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
            success:function () {
                window.location.href="/property_list/";
            },
            fail:function(){
                alert('删除失败!')
            }
        });

    });

    // ----编辑工具条----
    $('button[data-toggle="save"]').on('click', function () {
        // Todo 保存之前要做表单验证
        if ($(this).hasClass('disabled')) {

        } else {
            // $('.form-control').attr('readonly', true);
            // $('.custom-select').attr('disabled', true);
            // $('[data-toggle="tooltip"]').tooltip('disable');
            // $('button[data-toggle="save"]').addClass("disabled");
            // console.log($('form').serializeArray());
            $.post(
                "/property_form/",
                $('form').serialize(),
                function(context){
                    // window.location.href="/property_form?act=display&id="+context;
                    window.location.reload()
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
    $('.media').children('a').click(function (e) {
        e.preventDefault();
    });

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

    // ---- 输入修正 ----
    $('#sid').keyup(function () {
        // 转大写
        $(this).val($(this).val().toUpperCase());
    });

    // 输入建议
    $('#name').keyup(function () {
        // 只读时不产生后面的代码
        if ($(this).attr('readonly')) {
        } else {
            if($(this).val()) {
                var sch = $(this).val();
                var dlist = $('#indexname');
                $.get(
                    '/property_form/',
                    {act:'indexname', ilike:sch},
                    function(data) {
                        if(data.code === 0){
                            dlist.empty();
                            $.each(data.data,function (i,n) {
                                dlist.append('<option value="' + n['name'] + '"/>');
                            });
                        } else{
                            dlist.empty();
                        }
                    }
                    );
                $(this).removeClass('sr-only');
            }else{
                $('#indexname').addClass('sr-only');
            }
        }
    });

    $('#model').keyup(function () {
        if ($(this).attr('readonly')) {
        } else {
            var sch = $(this).val();
            var dlist = $('#indexmodel');
            if($(this).val()) {
                $.get(
                    '/property_form/',
                    {act:'indexmodel', ilike:sch},
                    function(data) {
                        if(data.code === 0){
                            dlist.empty();
                            $.each(data.data,function (i,n) {
                                dlist.append('<option value="' + n['model'] + '"/>');
                            });
                        } else{
                            dlist.empty();
                        }
                    }
                    );
                dlist.removeClass('sr-only');
            }else{
                dlist.addClass('sr-only');
            }
        }
    });

    $('#spec').keyup(function () {
        if ($(this).attr('readonly')) {
        } else {
            var sch = $(this).val();
            var dlist = $('#indexspec');
            if($(this).val()) {
                $.get(
                    '/property_form/',
                    {act:'indexspec', ilike:sch},
                    function(data) {
                        if(data.code === 0){
                            dlist.empty();
                            $.each(data.data,function (i,n) {
                                dlist.append('<option value="' + n['specifications'] + '"/>');
                            });
                        } else{
                            dlist.empty();
                        }
                    }
                    );
                dlist.removeClass('sr-only');
            }else{
                dlist.addClass('sr-only');
            }
        }
    });

    $('#position').keyup(function () {
        if ($(this).attr('readonly')) {
        } else {
            var sch = $(this).val();
            var dlist = $('#indexposition');
            if($(this).val()) {
                $.get(
                    '/property_form/',
                    {act:'indexposition', ilike:sch},
                    function(data) {
                        if(data.code === 0){
                            dlist.empty();
                            $.each(data.data,function (i,n) {
                                dlist.append('<option value="' + n['position'] + '"/>');
                            });
                        } else{
                            dlist.empty();
                        }
                    }
                    );
                dlist.removeClass('sr-only');
            }else{
                dlist.addClass('sr-only');
            }
        }
    });

    $('#categoryid').change(function () {
        //Todo 同时修改配件的继承性
        if($(this).val() == 0) {
            $(this).addClass('is-invalid');
            $('button[data-toggle="save"]').addClass("disabled");
        }else{
            $.get(
                '/property_form/',
                {act:'discategory', categoryid:$(this).val()},
                function(data) {
                    if(data.code === 0){
                        $('#categoryid').removeClass('is-invalid');
                        $('button[data-toggle="save"]').removeClass("disabled");
                        if( data.data['bom']){
                            $('#bom').prop("checked", true);
                        }else {
                            $('#bom').prop("checked", false);
                        }
                    }else{
                    }
                }
            );
        }
    });

    $('#user').change(function () {
        // 用户的部门职务信息
        if($(this).val() == 0) {
            $("#department").html("");
            $("#hrposition").html("");
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

    // ---- 表单验证 ----
    // --- name必填 ---
    $('#name').blur(function () {
        var me = $('#name');
        var pop = $('#popname');
        if (me.attr('readonly')) {
        } else {
            if($(this).val() == "") {
                me.addClass('is-invalid');
                $('button[data-toggle="save"]').addClass("disabled");
            }else{
                me.removeClass('is-invalid');
                $('button[data-toggle="save"]').removeClass("disabled");
            }
        }
    });

    // sid 必填、不重复
    $('#sid').blur(function () {
        var me = $('#sid');
        var pop = $('#popsid');
        var pk = $('#assetid').text();
        if(me.val() === "") {
            pop.text('必填');
            me.addClass('is-invalid');
            $('button[data-toggle="save"]').addClass("disabled");
        }else{
             $.get(
                 "/property_form",
                 {act:'chacksid',sid:$(this).val(), id:pk},
                 function (data) {
                     if (data.code === 0) {
                         $('button[data-toggle="save"]').removeClass("disabled");
                         me.removeClass('is-invalid');
                     } else {
                         $('button[data-toggle="save"]').addClass("disabled");
                         pop.text('此编号已存在');
                         me.addClass('is-invalid');
                     }
                 });
        }
    });

    // sn 必填、不重复、改o为0
    // 只读不验证
    // 当前记录不与本记录重复
    $('#sn').blur(function () {
        var me = $('#sn');
        var pop = $('#popsn');
        var pk = $('#assetid').text();
        console.log(pk);
        if (me.attr('readonly')) {
        } else {
            if (me.val() === "") {
                pop.text('必填');
                me.addClass('is-invalid');
                $('button[data-toggle="save"]').addClass("disabled");
            } else {
                $.get(
                    "/property_form",
                    {act: 'chacksn', sn: $(this).val(), id:pk},
                    function (data) {
                        if (data.code === 0) {
                            $('button[data-toggle="save"]').removeClass("disabled");
                            me.removeClass('is-invalid');
                        } else {
                            $('button[data-toggle="save"]').addClass("disabled");
                            pop.text('此编号已存在');
                            me.addClass('is-invalid');
                        }
                    });
            }
        }
    });

    //----配件添加----
    $('#addpart').click(function () {
        if ($(this).hasClass('disabled')) {
        } else {

            $.get("/property_form/",
                {act:"indexpartscategoryid"},
                function (data) {
                    if(data.code === 0){
                        var seloptl = $('#partscategoryid').selpartscategoryid(data.data);
                        $('#partscategoryid').empty();
                        $('#partscategoryid').append(seloptl);

                        var tabpartslist = $('#tabpartssel');
                        var categoryid = $('#partscategoryid');
                        var val = categoryid.val();

                        $.get("/property_list/",
                            {
                                act:"filter",
                                field:"categoryid",
                                ilike:val
                            },
                            function (data) {
                                var seloptl = "";
                                if(data.code === 0){
                                    seloptl = tabpartslist.tabpartsadd(data.data);
                                }else {
                                    seloptl = '<tr><td  colspan="5" style="text-align: center;">(暂无数据)</td></tr>';
                                }
                                tabpartslist.empty();
                                tabpartslist.append(seloptl);
                            }
                        );

                        }else {
                        var seloptl = '<option value="0">(请先指定哪些类型为配件)</option>';
                        $('#partscategoryid').empty();
                        $('#partscategoryid').append(seloptl);
                    }
                }
            );
            $('#Modalparts').modal("show");
        }
    });

    $('#tabpartlst').on('click','tr td button',function () {
        $.post("/property_form/",
            {
                act:"delparts",
                id:$(this).parent().parent().attr('data-id')
            },
            function (data) {
                // console.log(data);
                window.location.reload()
            }
        )
    });

    $('#partscategoryid').change(function () {
        //----重置添加按键----
        $('#partnum').html("0");
        $('#btnpartadd').addClass("disabled");

        var tabpartslist = $('#tabpartssel');
        var categoryid = $('#partscategoryid');
        var val = categoryid.val();

        $.get("/property_list/",
            {
                act:"filter",
                field:"categoryid",
                ilike:val
            },
            function (data) {
                var seloptl = "";
                if(data.code === 0){
                    seloptl = tabpartslist.tabpartsadd(data.data);
                }else {
                    seloptl = '<tr><td  colspan="5" style="text-align: center;">(暂无数据)</td></tr>';
                }
                tabpartslist.empty();
                tabpartslist.append(seloptl);
            }
        );
    });

    // ----勾选----
    $('#tabpartssel').on("click","tr td input",function () {
        var tabpartslist = $('#tabpartssel');
        var sel = $(this).prop("checked");
        var i = $('#partnum').html();
        i=parseInt(i);

        if (sel){
            $(this).prop("checked", true);
            $('#btnpartadd').removeClass("disabled");
            i=i+1;
            $('#partnum').html(i);
        }else{
            $(this).prop("checked", false);
            i=i-1;
            $('#partnum').html(i);
            if(!i){
                $('#btnpartadd').addClass("disabled");
            }
        }
    });

    $('#btnpartadd').click(function () {
        var chkbox = $('#tabpartssel tr td input');
        var addid = "";
        if ($(this).hasClass('disabled')) {
        } else {
            chkbox.each(function(){
                if( $(this).prop("checked")){
                    console.log($(this).val());
                    addid = addid + $(this).val() + ","
                }
            });
            $.post("/property_form/",
                {
                    act:"addparts",
                    id:addid,
                    parentid:$("#id").val()
                },
                function (data) {
                console.log(data);
                $('#Modalparts').modal('hide');
                window.location.reload();
                }
            );

        }
    });
});