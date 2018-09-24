$(document).ready(function () {
    $('tbody tr td').click(function () {
         if ( $(this).index() > 0 ){
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
                $('tbody').empty()
                var json=[{"id":"1","name":"n1"},{"id":"2","name":"n2"}]

                for (var k in data) {
                    console.log('llll')
                    console.log(data[k]);
                }
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

