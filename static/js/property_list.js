$(document).ready(function () {
    //-----控制面板----
    $('#search-input').bind('keypress',function(event){
        if(event.keyCode === 13)
        {
            return $('#search-btn').click();
        }
    });

    $('#search-btn').click(function () {
        var val= $('#search-input').val();
        // if (val ===  ""){
        //     return;
        // }
        $.get(
            '/property_list/',
            {
                act:'filter',
                field:'name',
                ilike:val
            },
            function (data) {
                var htxt = "";
                if(data.code === 0) {
                    $.each(data.data, function (i, n) {
                        if ((n['user__name'] != null) && (n["user__active"] == 0)) {
                            htxt += '<tr class="text-danger">';
                        } else {
                            htxt += '<tr>';
                        }
                        htxt += '<td><input type="checkbox" name="selitem" value="' + n["id"] + '"></td>';
                        if (n["status"] === 1) {
                            htxt += "<td><span class=\"badge badge-secondary\">闲置</span></td>";
                        } else if (n["status"] === 2) {
                            htxt += "<td><span class=\"badge badge-success\">在用</span></td>";
                        } else if (n["status"] === 3) {
                            htxt += "<td><span class=\"badge badge-warning\">维修</span></td>";
                        } else if (n["status"] === 4) {
                            htxt += "<td><span class=\"badge badge-danger\">报废</span></td>";
                        }
                        htxt += "<td>" + n["sid"] + "</td>";
                        htxt += "<td>" + n["name"] + "</td>";

                        if (n["specifications"] === null) {
                            htxt += "<td></td>";
                        } else {
                            htxt += "<td>" + n["specifications"] + "</td>";
                        }
                        if (n["sn"] === null) {
                            htxt += "<td></td>";
                        } else {
                            htxt += "<td>" + n["sn"] + "</td>";
                        }
                        if (n["purchase"] === null) {
                            htxt += "<td></td>";
                        } else {
                            htxt += "<td>" + n["purchase"] + "</td>";
                        }
                        if (n["warranty"] === null) {
                            htxt += "<td></td>";
                        } else {
                            htxt += "<td>" + n["warranty"] + "</td>";
                        }
                        if (n["user__name"] === null) {
                            htxt += "<td></td>";
                        } else {
                            htxt += "<td>" + n["user__name"] + "</td>";
                        }
                        if (n["position"] === null) {
                            htxt += "<td></td>";
                        } else {
                            htxt += "<td>" + n["position"] + "</td>";
                        }

                        htxt += '</tr>';
                    });
                }else{
                    htxt = '<tr><td  colspan="10" style="text-align: center;">(暂无数据)</td></tr>'
                }
                console.log(htxt);
                $('tbody').empty();
                $("tbody").append(htxt);
            }
        );
    });

    // $('#search-input').input(function () {
    //     var val= $('#search-input').val();
    //     console.log(val);
    // });

    $('button[data-toggle="create"]').click(function () {
        if ($(this).hasClass('disabled')) {

        } else {
            $(location).attr('href', '/property_form?act=create&id=0');
        }
    });

    $('button[data-toggle="del"]').on('click',function () {
        if ($(this).hasClass('disabled')) {

        }else{
            $('#delnum').html($('input[name="selall"]').val());
            $('#Mdadel').modal('show');
        }
    });

    $('button[data-toggle="surdel"]').click(function () {
        $('input[name="selitem"]').each(function () {
            if ($(this).prop("checked")) {
                var asid = $(this).val();
                var idx = $(this).parents("tr").index();
                $.ajax({
                    url: "/property_form/",
                    type: "POST",
                    data: {
                        "act": "unactive",
                        "id": asid
                    }
                });
                $(this).parents("tr").empty();
            }
        });
        $('input[name="selall"]').val(0);
        $('button[data-toggle="del"]').addClass("disabled");
        $('#Mdadel').modal('hide');
    });

    //<!--导入导出条-->
    $('#dddd').click(function () {

        $('.progress-bar').css("width","0%");
        $('#MdaInput').modal('show');
    });

    $('#customFile').change(function () {
        $('.custom-file-label').html($('#customFile').val());
    });

    $('button[data-toggle="surinput"]').click(function () {
        function progressBar(evt) {
            var loaded = evt.loaded; //已经上传大小情况
            var tot = evt.total; //附件总大小
            var per = Math.floor(100 * loaded / tot); //已经上传的百分比
            //绘制经度条
            var pr = per + '%';
            $('.progress-bar').css("width",pr);
            $('.progress-bar').html(pr);
        }
        $.ajax({
            url:"/upload/",
            type:"post",
            cache: false,
            async:true,
            data:new FormData($('#forminput')[0]),
            processData: false,
            contentType: false,
            xhr: function () {
                var xhr = $.ajaxSettings.xhr();
                if (xhr.upload) {
                    xhr.upload.addEventListener("progress", progressBar, false);
                    return xhr;
                }
            },
            success: function(req) {
                //请求成功时处理
                $('.progress-bar').html('完成');
                $('#MdaInput').modal('hide');
            }
        });
    });

    //---- 排序 ----
    $('th').click(function () {
        if ( $(this).index() > 0 ) {

            var obj = $(this).find('i');
            var alli = $('th i');
            var sortitem = $(this).attr("data-id");

            alli.removeClass("fa fa-sort-alpha-asc");
            alli.removeClass("fa fa-sort-alpha-desc");

            if (obj.attr('data-id') == 0) {
                alli.attr('data-id', 0);

                obj.attr('data-id', 1);
                obj.addClass("fa fa-sort-alpha-asc");
                sortitem = sortitem;
            } else if (obj.attr('data-id') == 1) {
                alli.attr('data-id', 0);

                obj.attr('data-id', 2);
                obj.addClass("fa fa-sort-alpha-desc");
                sortitem = "-" + sortitem;
            } else if (obj.attr('data-id') == 2) {
                alli.attr('data-id', 0);

                $('th[data-id="name"] i').addClass("fa fa-sort-alpha-asc");
                $('th[data-id="name"] i').attr('data-id', 1);
                sortitem = "name";
            }

            $.ajax({
                url: "/property_list/",
                type: "POST",
                data: {
                    "act": 'sort',
                    "Field": sortitem
                },
                success: function (data) {
                    $('input[name="selall"]').prop("checked", false);

                    var htxt = "";
                    $.each(data,function (i,n) {
                        // if((n['user__name'] != null) && (n["user__active"] == 0)) {
                        //     $("tbody").append('<tr class="text-danger"></tr>');
                        // } else {
                        //     $("tbody").append('<tr></tr>');
                        // }
                        //
                        // var rrow =$("tbody tr:last");
                        // rrow.append('<td><input type="checkbox" name="selitem" value="'+ n["id"] +'"></td>');
                        // if (n["status"] == 1) {
                        //     rrow.append("<td><span class=\"badge badge-secondary\">闲置</span></td>");
                        // }else if (n["status"] == 2) {
                        //     rrow.append("<td><span class=\"badge badge-success\">在用</span></td>");
                        // }else if (n["status"] == 3) {
                        //     rrow.append("<td><span class=\"badge badge-warning\">维修</span></td>");
                        // } else if (n["status"] == 4) {
                        //     rrow.append("<td><span class=\"badge badge-danger\">报废</span></td>");
                        // }
                        // rrow.append("<td>" + n["sid"] + "</td>");
                        // rrow.append("<td>" + n["name"] + "</td>");
                        //
                        // if (n["specifications"] == null) {
                        //     rrow.append("<td></td>");
                        // } else {
                        //     rrow.append("<td>" + n["specifications"] + "</td>");
                        // }
                        //
                        // if (n["sn"] == null) {
                        //     rrow.append("<td></td>");
                        // } else {
                        //     rrow.append("<td>" + n["sn"] + "</td>");
                        // }
                        //
                        // rrow.append("<td>" + n["purchase"] + "</td>");
                        // rrow.append("<td>" + n["warranty"] + "</td>");
                        //
                        // if (n["user__name"] == null) {
                        //     rrow.append("<td></td>");
                        // } else {
                        //     rrow.append("<td>" + n["user__name"] + "</td>");
                        // }
                        //
                        // if (n["position"] == null) {
                        //     rrow.append("<td></td>");
                        // } else {
                        //     rrow.append("<td>" + n["position"] + "</td>");
                        // }

                        if((n['user__name'] != null) && (n["user__active"] == 0)) {
                            htxt += '<tr class="text-danger">';
                        } else {
                            htxt += '<tr>';
                        }
                        htxt += '<td><input type="checkbox" name="selitem" value="'+ n["id"] +'"></td>';
                        if (n["status"] === 1) {
                            htxt += "<td><span class=\"badge badge-secondary\">闲置</span></td>";
                        }else if (n["status"] === 2) {
                             htxt += "<td><span class=\"badge badge-success\">在用</span></td>";
                        }else if (n["status"] === 3) {
                             htxt += "<td><span class=\"badge badge-warning\">维修</span></td>";
                        } else if (n["status"] === 4) {
                             htxt += "<td><span class=\"badge badge-danger\">报废</span></td>";
                        }
                        htxt += "<td>" + n["sid"] + "</td>";
                        htxt += "<td>" + n["name"] + "</td>";

                        if (n["specifications"] === null) {
                            htxt += "<td></td>";
                        } else {
                            htxt += "<td>" + n["specifications"] + "</td>";
                        }
                        if (n["sn"] === null) {
                            htxt += "<td></td>";
                        } else {
                            htxt += "<td>" + n["sn"] + "</td>";
                        }
                        if (n["purchase"] === null) {
                            htxt += "<td></td>";
                        } else {
                            htxt += "<td>" + n["purchase"] + "</td>";
                        }
                        if (n["warranty"] === null) {
                            htxt += "<td></td>";
                        } else {
                            htxt += "<td>" + n["warranty"] + "</td>";
                        }
                        if (n["user__name"] === null) {
                            htxt += "<td></td>";
                        } else {
                            htxt += "<td>" + n["user__name"] + "</td>";
                        }
                        if (n["position"] === null) {
                            htxt += "<td></td>";
                        } else {
                            htxt += "<td>" + n["position"] + "</td>";
                        }

                        htxt += '</tr>';
                    });
                    $('tbody').empty();
                    $("tbody").append(htxt);

                    $('input[name="selitem"]').prop("checked", false);
                    $('button[data-toggle="del"]').addClass("disabled");
                    $('input[name="selall"]').val(0);
                }
            });
        }
    });

    //----点选----
    // $("tbody tr td:first-child").nextAll().css('background','blue');
    // $("tbody tr td:not(:first-child)").css('background','blue');

    $("tbody").on("click","tr td:not(:first-child)",function () {
        var showsel = $(this).siblings().eq(0).find('input').val();
        window.location.href="/property_form?act=display&id="+showsel;
    });

    $('input[name="selall"]').click(function () {
        var i =0;
        if ($(this).prop("checked")){
            $('input[name="selitem"]').each(function () {
                $(this).prop("checked", true);
                i=i+1;
            });
            $('button[data-toggle="del"]').removeClass("disabled");
        }else{
            $('input[name="selitem"]').each(function () {
                $(this).prop("checked", false);
            });
            $('button[data-toggle="del"]').addClass("disabled");
        }
        $('input[name="selall"]').val(i);
    });

    $('tbody').on("click","tr td input",function () {
                $(this).css("background","blue");
       var sel = $(this).prop("checked");
       var i = $('input[name="selall"]').val();
       i=parseInt(i);

        if (sel){
            $(this).prop("checked", true);
            $('button[data-toggle="del"]').removeClass("disabled");
            i=i+1;
            $('input[name="selall"]').val(i);
        }else{
            $('input[name="selall"]').prop("checked", false);
            $(this).prop("checked", false);
            i=i-1;
            $('input[name="selall"]').val(i);
            if(!i){
                $('button[data-toggle="del"]').addClass("disabled");
            }
        }
    });
});

