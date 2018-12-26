$(document).ready(function () {
    init('页面初始化');

    // ----编辑工具条----
    $('#goback').on('click', function () {
        if ($(this).hasClass('disabled')) {

        } else {
            window.location.href = "/pure_list/";
        }
    });
});

function init(obj) {
    // console.log(obj);
}