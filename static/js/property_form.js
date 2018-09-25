$(document).ready(function () {
    $('.form-control, .custom-select').attr('readonly',true);

    $('#cateid').on('click',function () {
        $('#myModal').modal("show");
    });

    $('button[data-toggle="edit"]').on('click',function () {
        if ($(this).hasClass('disabled')) {

        }else{
            $('.form-control, .custom-select').removeAttr('readonly',true);
            $('button[data-toggle="save"]').removeClass("disabled");
        }
    });

    $('button[data-toggle="create"]').on('click',function () {
        if ($(this).hasClass('disabled')) {

        }else{
            alert("create");
        }
    });

    $('button[data-toggle="del"]').on('click',function () {
        if ($(this).hasClass('disabled')) {

        }else{
            $('#Md_del').modal("show");
        }
    });

    $('button[data-toggle="save"]').on('click',function () {
        if ($(this).hasClass('disabled')) {

        }else{
            alert("提交中,请等待...");
            $('.form-control, .custom-select').attr('readonly',true);
            $('button[data-toggle="save"]').addClass("disabled");
        }
    });

    $('button[data-toggle="goback"]').on('click',function () {
        if ($(this).hasClass('disabled')) {

        }else{
            $('.form-control, .custom-select').attr('readonly',true);
            $('button[data-toggle="save"]').addClass("disabled");
            window.location.href="/property_list/";
        }
    });
});
