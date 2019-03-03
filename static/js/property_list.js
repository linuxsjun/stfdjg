$(function () {
    function dataload() {
        var juk=$('form#panl').serialize();
        $('#dbody').load(
            '/property_list/ #sub',
            juk,
            function (context) {
                // console.log(context)
            }
        );
    }
    init('页面初始化');
    // ----扩展函数----
    $.fn.extend({
        'listitem': function (data) {
            var htxt = "";
            $.each(data, function (i, n) {
                if ((n['user__name'] != null) && (n["user__active"] == 0)) {
                    htxt += '<tr class="text-danger listitem">';
                } else {
                    htxt += '<tr class="listitem">';
                }
                htxt += '<td><input type="checkbox" name="selitem" value="' + n["id"] + '"></td>';
                if (n["status"] === 1) {
                    htxt += '<td><span class=\"badge badge-secondary\">闲置</span></td>';
                } else if (n["status"] === 2) {
                    htxt += '<td><span class=\"badge badge-success\">在用</span></td>';
                } else if (n["status"] === 3) {
                    htxt += '<td><span class=\"badge badge-warning\">维修</span></td>';
                } else if (n["status"] === 4) {
                    htxt += '<td><span class=\"badge badge-danger\">报废</span></td>';
                }
                htxt += '<td>' + n["sid"] + "</td>";
                htxt += '<td>' + n["name"] + "</td>";

                if (n["specifications"] === null) {
                    htxt += '<td></td>';
                } else {
                    htxt += '<td>' + n["specifications"] + "</td>";
                }
                if (n["sn"] === null) {
                    htxt += '<td></td>';
                } else {
                    htxt += '<td>' + n["sn"] + "</td>";
                }

                if (n["warranty"] === null) {
                    htxt += '<td></td>';
                } else {
                    htxt += '<td>' + n["warranty"] + "</td>";
                }
                if (n["user__name"] === null) {
                    htxt += '<td></td>';
                } else {
                    htxt += '<td>' + n["user__name"] + "</td>";
                }
                // if ((n["user__employee_department__departmentid__name"] === null) || (n["user__employee_department__departmentid__name"] === None)) {
                htxt += '<td></td>';
                // } else {
                //     htxt += '<td>' + n["user__employee_department__departmentid__name"] + "</td>";
                // }
                if (n["position"] === null) {
                    htxt += '<td></td>';
                } else {
                    htxt += '<td>' + n["position"] + "</td>";
                }
                htxt += '</tr>';
            });
            return htxt;
        },
        'groupitem': function (data) {
            var htxt = "";
            $.each(data, function (i, n) {
                htxt += '<tr class="groupitem text-primary bg-white bg-gradient-warning shadow" data-dropdown="0" data-val="' + n["val"] + '">';
                // htxt += '<tr class="groupitem text-primary bg-white bg-gradient-warning shadow" data-dropdown="0" data-disn="' + n["disn"] + '" data-val="' + n["val"] + '">';
                htxt += '<td colspan="10"><i class="fa fa-caret-right fa-1x"></i> <span data-groupby="' + n["field"] + '">' + n["disn"] + '</span> <b>(' + n["number"] + ') </b></td>'
                htxt += '</tr>';
            });
            $(this).empty();
            $(this).append(htxt);
            return htxt;
        }
    });

    //-----控制面板----

    // ------查找------
    $('#search-input').bind('keypress', function (event) {
        if (event.keyCode === 13) {
            $('#search-btn').trigger('click');
        }

    });

    $('#search-btn').click(function () {
        var val = $('#search-input').val();
        $('#ilike').val(val);
        $('#test').trigger('click');
    });

    // -----命令按键----
    $('button[data-toggle="create"]').click(function () {
        if ($(this).hasClass('disabled')) {

        } else {
            $(location).attr('href', '/property_form?act=create&id=0');
        }
    });

    $('button[data-toggle="del"]').on('click', function () {
        if ($(this).hasClass('disabled')) {

        } else {
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

        $('.progress-bar').css("width", "0%");
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
            $('.progress-bar').css("width", pr);
            $('.progress-bar').html(pr);
        }

        $.ajax({
            url: "/upload/",
            type: "post",
            cache: false,
            async: true,
            data: new FormData($('#forminput')[0]),
            processData: false,
            contentType: false,
            xhr: function () {
                var xhr = $.ajaxSettings.xhr();
                if (xhr.upload) {
                    xhr.upload.addEventListener("progress", progressBar, false);
                    return xhr;
                }
            },
            success: function (req) {
                //请求成功时处理
                $('.progress-bar').html('完成');
                $('#MdaInput').modal('hide');
            }
        });
    });

    // ----筛选----
    $('#unactive').click(function (event) {
        event.preventDefault();

        var eact = $('#act');
        if (eact.val() === '1') {
            eact.val('0');
        } else {
            eact.val('1');
        }
        $(this).children('span').toggleClass('sr-only');
        $('#test').trigger('click');
    });

    //----分组----
    $('[data-act="group"]').click(function (event) {
        event.preventDefault();

        var byf = $(this).attr("data-groupby");
        $.get(
            "/property_list/",
            {
                act: "groupby",
                field: byf
            },
            function (data) {
                if (data.code === 0) {
                    $('#assetid').text("0-0/" + data.spk);
                    $('tbody').groupitem(data.data);
                } else {
                    $('#assetid').text("0-0/0");
                    var htext = '<tr><td  colspan="10" style="text-align: center;">(暂无数据)</td></tr>';
                    $('tbody').empty().append(htext);
                }

                // $('input[name="selitem"]').prop("checked", false);
                // $('button[data-toggle="del"]').addClass("disabled");
                // $('input[name="selall"]').val(0);
            }
        );
    });

    // ----上下页----
    $('#dbody').on('click', '[aria-label="Previous"]', function (event) {
        event.preventDefault();
        $('#page').val($(this).attr('data-pagprevious'));
        $('#test').trigger('click');
    });

    $('#dbody').on('click', '[aria-label="Next"]', function (event) {
        event.preventDefault();
        $('#page').val($(this).attr('data-pagnext'));
        $('#test').trigger('click');
    });


    // ----视图类型----
    $('#dbody').on('change', '#viewtype label input[type="radio"]', function () {
        var val=$(this).val();
        $('#tview').val(val);
        $('#test').trigger('click');
    });

    //---- 排序 ----
    $('#dbody').on('click', 'th', function () {
        if ($(this).index() > 0) {
            var sortitem = $(this).attr("data-id");
            $('#orderby').val(sortitem);
            $('#test').trigger('click');

            // console.log($(this).css("background-color","yellow"));
            // $(this).css("background-color","yellow");
        }
    });

    $('th').click(function () {
        if ($(this).index() > 0) {
            var obj = $(this).find('i');
            var alli = $('th i');
            var sortitem = $(this).attr("data-id");

            alli.removeClass("fa fa-sort-alpha-asc");
            alli.removeClass("fa fa-sort-alpha-desc");

            if (obj.attr('data-id') === "0") {
                alli.attr('data-id', 0);

                obj.attr('data-id', 1);
                obj.addClass("fa fa-sort-alpha-asc");
                sortitem = sortitem;
            } else if (obj.attr('data-id') === "1") {
                alli.attr('data-id', 0);

                obj.attr('data-id', 2);
                obj.addClass("fa fa-sort-alpha-desc");
                sortitem = "-" + sortitem;
            } else if (obj.attr('data-id') === "2") {
                alli.attr('data-id', 0);

                $('th[data-id="name"] i').addClass("fa fa-sort-alpha-asc");
                $('th[data-id="name"] i').attr('data-id', 1);
                sortitem = "name";
            }

            // $.ajax({
            //     url: "/property_list/",
            //     type: "GET",
            //     data: {
            //         "act": 'sort',
            //         "field": sortitem
            //     },
            //     success: function (data) {
            //         $('input[name="selall"]').prop("checked", false);
            //
            //         $('#assetid').text("0-0/" + data.spk);
            //         var htext = $(this).listitem(data.data);
            //         $('tbody').empty();
            //         $("tbody").append(htext);
            //
            //         $('input[name="selitem"]').prop("checked", false);
            //         $('button[data-toggle="del"]').addClass("disabled");
            //         $('input[name="selall"]').val(0);
            //     }
            // });
        }
    });

    //----点选----
    // ----分组点选----
    $("#dbody").on("click", "tr.groupitem td", function () {
        var tritem = $(this).parent();
        var ilike = tritem.attr("data-val");
        var field = tritem.find('span').attr("data-groupby");
        var chitem = tritem.attr("data-dropdown");
        // print(ilike);
        if (chitem === "0") {
            $.get(
                "/property_list/",
                {
                    act: "filter",
                    field: field,
                    ilike: ilike
                },
                function (data) {
                    if (data.code === 0) {
                        $('#assetid').text("0-0/0");
                        var trlist = $('tbody').listitem(data.data);
                        tritem.after(trlist);
                        tritem.attr("data-dropdown", data.spk)
                    } else {
                        $('#assetid').text("0-0/0");
                        var trlist = '<tr><td  colspan="10" style="text-align: center;">(暂无数据)</td></tr>';
                        tritem.after(trlist);
                        tritem.attr("data-dropdown", 1)
                    }
                }
            );
            $(this).children("i").addClass("fa-caret-down");
            $(this).children("i").removeClass("fa-caret-right");
        } else {
            for (var i = 0; i < chitem; i++) {
                tritem.next().remove();
                tritem.attr("data-dropdown", 0);
            }
            $(this).children("i").addClass("fa-caret-right");
            $(this).children("i").removeClass("fa-caret-down");
        }

    });

    // ----条目点选----
    $("#dbody").on("click", "tr.listitem td:not(:first-child)", function () {
        var showsel = $(this).parent().find('[name="selitem"]').val();
        // window.location.href="/property_form?act=display&id="+showsel;
        window.open("/property_form?act=display&id=" + showsel);
    });

    // ----勾选----
    $('#dbody').on('click', 'input[name="selall"]', function () {
        var i = 0;
        if ($(this).prop("checked")) {
            $('input[name="selitem"]').each(function () {
                $(this).prop("checked", true);
                i = i + 1;
            });
            $('button[data-toggle="del"]').removeClass("disabled");
        } else {
            $('input[name="selitem"]').each(function () {
                $(this).prop("checked", false);
            });
            $('button[data-toggle="del"]').addClass("disabled");
        }
        $('input[name="selall"]').val(i);
    });

    $('#dbody').on("click", "tr td input", function () {
        var sel = $(this).prop("checked");
        var i = $('input[name="selall"]').val();
        i = parseInt(i);

        if (sel) {
            $(this).prop("checked", true);
            $('button[data-toggle="del"]').removeClass("disabled");
            i = i + 1;
            $('input[name="selall"]').val(i);
        } else {
            $('input[name="selall"]').prop("checked", false);
            $(this).prop("checked", false);
            i = i - 1;
            $('input[name="selall"]').val(i);
            if (!i) {
                $('button[data-toggle="del"]').addClass("disabled");
            }
        }
    });

    $('#test').on('click', function () {
        dataload()
    });

});
function init(obj) {
    // 激活sideMenu
    var navitem = $('nav').find('.nav-link');
    navitem.removeClass('active');
    $('#menu02').addClass('active');
    $('#menu020301').addClass('active');
}
