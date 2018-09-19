$(document).ready(function () {
    $('tbody tr').click(function () {
         var showsel = $(this).find('td input').val();
         window.location.href="/property_form?act=display&id="+showsel;
    });

    $('button[data-toggle="create"]').on('click',function () {
        alert("create")
    });

    $('button[data-toggle="del"]').on('click',function () {
        alert("del")
    });

    <!-- sort -->
    $('thead > tr > th').click(function () {
        var obj =$(this).find('span');

        if (obj.hasClass("caret")){
            obj.removeClass("caret");
            console.log("-" + $(this).attr("data-id"));
        }else{
            $('thead > tr > th > span').removeClass("caret");
            obj.addClass("caret");
            console.log($(this).attr("data-id"));
        }
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

