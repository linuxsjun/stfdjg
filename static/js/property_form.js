$(document).ready(function () {
    $('.sheet>div>div').css("display","none");
    $($('.sheet>div>div')[0]).css("display","block");
    $('.sheet>ul>li>a').click(function () {
        $('.sheet>ul>li').removeClass("active");
        $(this).parent().addClass("active");

        $('.sheetcontext>div').css("display","none");
        $('.sheetcontext>div')[$(this).parent().index()].style.display='block'
    })
})
