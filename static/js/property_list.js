$(document).ready(function () {
    $('tbody tr').dblclick(function () {
         var showsel = $(this).find('td input').val();
         window.location.href="/property_form?act=display&id="+showsel;
    });

    $('button[data-toggle="create"]').click(function () {
        alert("create")
    });

    $('button[data-toggle="del"]').click(function () {
        alert("del")
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

