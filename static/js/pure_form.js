$(document).ready(function () {

    // ----编辑工具条----
    $('#goback').on('click', function () {
        if ($(this).hasClass('disabled')) {

        } else {
            window.location.href = "/pure_list/";
        }
    });
});
