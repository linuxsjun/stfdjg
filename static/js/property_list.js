$(document).ready(function () {
    $('tbody tr td').click(function () {
         if ( $(this).index() > 0 ){
             console.log('kkkk')
             var showsel = $(this).siblings().eq(0).find('input').val();
             window.location.href="/property_form?act=display&id="+showsel;
         }
    });

    $('button[data-toggle="create"]').on('click',function () {
        // alert("create");
        $.ajax({
            url:"/property_list/",
            type:"POST",
            data:{
                "act":'sort',
                "Field":"sn"
            },
            success:function (data) {
                // console.log($(tbody).text())
                // $('tbody').empty()
                $('tbody').remove();
                var disdatas="<tbody>";
                var disdat;

                for (var k in data) {
                    disdat='<tr><td><input type=\"checkbox\" name=\"selitem\" value=\"'+data[k]["id"]+'\"></td><td><span class=\"badge badge-success\">'+data[k]["status"]+"</span></td><td>"+data[k]["sid"]+"</td><td>"+data[k]["name"]+"</td><td>"+data[k]["specifications"]+"</td><td>"+data[k]["sn"]+"</td><td>"+data[k]["purchase"]+"</td><td>"+data[k]["warranty"]+"</td><td>"+data[k]["user__name"]+"</td></tr>";
                    disdatas=disdatas+disdat;
                    // console.log(data[k]);
                }
                // $('thead').after("<tbody><tr><td colspan=\"9\" style=\"text-align\: center;\">(暂无数据)</td></tr></tbody>");
                disdatas=disdatas+"</tbody>";
                $('thead').after(disdatas);
            }
        })
    });

    $('button[data-toggle="del"]').on('click',function () {
        if ($(this).hasClass('disabled')) {

        }else{
            alert("del")
        }
    });

    <!-- sort -->
    $('thead > tr > th').click(function () {
        var obj =$(this).find('i');

        obj.removeClass("fa fa-sort-alpha-asc");
        obj.removeClass("fa fa-sort-alpha-desc");

        if (obj.attr('data-id') == 0){
            obj.attr('data-id',1);
            obj.addClass("fa fa-sort-alpha-asc");
        }else {
            if (obj.attr('data-id') == 1) {
                obj.attr('data-id',2);
                obj.addClass("fa fa-sort-alpha-desc");
            }else {
                obj.attr('data-id',0);
                obj.removeClass("fa fa-sort-alpha-asc");
            }
        }
        console.log(obj.attr('data-id'));
        console.log($(this).attr("data-id"));
    });

    $('input[name="selall"]').click(function () {
        var sel = $(this).prop("checked");
        if (sel){
            $('input[name="selitem"]').attr("checked", true)
        }else{
            $('input[name="selitem"]').attr("checked", false);
        }

    });

    $('input[name="selitem"]').click(function () {
       var sel = $(this).prop("checked");
        if (sel){
            $(this).attr("checked", true);
        }else{
            $(this).attr("checked", false);
        }
    });
});

