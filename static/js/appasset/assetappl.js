$(function () {

    //领用、借用切换
    $("#radiotypeaccess").change(function () {
        $("#borrowdate").toggleClass("sr-only")
    });
    $("#radiotypeborrow").change(function () {
        $("#borrowdate").toggleClass("sr-only")
    });

    // submit
    $("#submit").click(function () {
        $.post("/asset/assetappl/",
            $('form').serialize(),
            function (data) {

            });
    });
});