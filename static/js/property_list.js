$(document).ready(function () {


    $('button[data-toggle="create"]').on('click',function () {
        // alert("create");

    });

    $('button[data-toggle="del"]').on('click',function () {
        if ($(this).hasClass('disabled')) {

        }else{
            var i = $('input[name="selall"]').val();
            $('#delnum').html(i);
            $('#sssss').modal('show');
        }
    });

    $('button[data-toggle="surdel"]').click(function () {
        $('#sssss').modal('hide');
        $('input[name="selitem"]').each(function () {
            if ($(this).prop("checked")) {
                var asid = $(this).val();
                $.ajax({
                    url: "/property_form/",
                    type: "POST",
                    data: {
                        "act": "unactive",
                        "id": asid
                    },
                    success: function (data) {
                        // $(this).parents("tr").empty();
                    }
                });
                $(this).parents("tr").empty();
            }
        });
        $('input[name="selall"]').val(0);
        $('button[data-toggle="del"]').addClass("disabled");
    });

    $('#dddd').click(function () {
        alert('kkkkk');
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

                    $('tbody').remove();

                    var disdat;

                    var disdatas = "<tbody>";
                    for (var k in data) {
                        disdat = '<td><input type=\"checkbox\" name=\"selitem\" value=\"' + data[k]["id"] + '\"></td>';
                        if (data[k]["status"] == 1) {
                            disdat = disdat + "<td><span class=\"badge badge-secondary\">闲置</span></td>";
                        } else if (data[k]["status"] == 2) {
                            disdat = disdat + "<td><span class=\"badge badge-success\">在用</span></td>";
                        } else if (data[k]["status"] == 3) {
                            disdat = disdat + "<td><span class=\"badge badge-warning\">维修</span></td>";
                        } else if (data[k]["status"] == 4) {
                            disdat = disdat + "<td><span class=\"badge badge-danger\">报废</span></td>";
                        }
                        disdat = disdat + "<td>" + data[k]["sid"] + "</td><td>" + data[k]["name"] + "</td>";

                        if (data[k]["specifications"] == null) {
                            disdat = disdat + "<td></td>";
                        } else {
                            disdat = disdat + "<td>" + data[k]["specifications"] + "</td>";
                        }

                        if (data[k]["sn"] == null) {
                            disdat = disdat + "<td></td>";
                        } else {
                            disdat = disdat + "<td>" + data[k]["sn"] + "</td>";
                        }

                        disdat = disdat + "<td>" + data[k]["purchase"] + "</td><td>" + data[k]["warranty"] + "</td>";
                        if (data[k]["user__name"] == null) {
                            disdat = disdat + "<td></td>";
                        } else {
                            if (data[k]["user__active"]) {
                                disdat = disdat + "<td>" + data[k]["user__name"] + "</td>";
                            } else {
                                disdat = disdat + "<td><span class=\"badge badge-danger\">" + data[k]["user__name"] + "</span></td>";
                            }
                        }
                        disdatas = disdatas + "<tr>" + disdat + "</tr>";
                    }
                    disdatas = disdatas + "</tbody>";

                    $('thead').after(disdatas);

                    $('tbody tr td').click(function () {
                        if ($(this).index() > 0) {
                            var showsel = $(this).siblings().eq(0).find('input').val();
                            window.location.href = "/property_form?act=display&id=" + showsel;
                        }
                    });

                    $('input[name="selitem"]').prop("checked", false);
                    $('button[data-toggle="del"]').addClass("disabled");
                    $('input[name="selall"]').val(0);

                    $('input[name="selall"]').click(function () {
                        var sel = $(this).prop("checked");
                        var i =0;

                        if (sel){
                            $('input[name="selitem"]').prop("checked", true);
                            $('button[data-toggle="del"]').removeClass("disabled");

                            $('input[name="selitem"]').each(function () {
                                i=i+1;
                            });
                        }else{
                            $('input[name="selitem"]').prop("checked", false);
                            $('button[data-toggle="del"]').addClass("disabled");
                        }
                        $('input[name="selall"]').val(i);
                    });

                    $('input[name="selitem"]').click(function () {
                       var sel = $(this).prop("checked");
                       var i = $('input[name="selall"]').val();
                       i=parseInt(i);

                        if (sel){
                            $(this).prop("checked", true);
                            $('button[data-toggle="del"]').removeClass("disabled");
                            i=i+1;
                            $('input[name="selall"]').val(i);
                        }else{
                            $(this).prop("checked", false);
                            i=i-1;
                            $('input[name="selall"]').val(i);
                            if(!i){
                                $('button[data-toggle="del"]').addClass("disabled");
                            }
                        }
                    });
                }
            });
        }
    });

    //----点选----
    $('tbody tr td').click(function () {
         if ( $(this).index() > 0 ){
             var showsel = $(this).siblings().eq(0).find('input').val();
             window.location.href="/property_form?act=display&id="+showsel;
         }
    });

    $('input[name="selall"]').click(function () {
        var sel = $(this).prop("checked");
        var i =0;

        if (sel){
            $('input[name="selitem"]').prop("checked", true);
            $('button[data-toggle="del"]').removeClass("disabled");

            $('input[name="selitem"]').each(function () {
                i=i+1;
            });
        }else{
            $('input[name="selitem"]').prop("checked", false);
            $('button[data-toggle="del"]').addClass("disabled");
        }
        $('input[name="selall"]').val(i);
    });

    $('input[name="selitem"]').click(function () {
       var sel = $(this).prop("checked");
       var i = $('input[name="selall"]').val();
       i=parseInt(i);

        if (sel){
            $(this).prop("checked", true);
            $('button[data-toggle="del"]').removeClass("disabled");
            i=i+1;
            $('input[name="selall"]').val(i);
        }else{
            $(this).prop("checked", false);
            i=i-1;
            $('input[name="selall"]').val(i);
            if(!i){
                $('button[data-toggle="del"]').addClass("disabled");
            }
        }
    });
});

