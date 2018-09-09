$(document).ready(function () {
    $('.sheet>div>div').css("display","none")
    $($('.sheet>div>div')[0]).css("display","block")
    $('.sheet>ul>li>a').click(function () {
        $('.sheet>ul>li>a').css("background","#dddddd")

        // // alert($(this).index())
        $(this).css("background","white")

        $('.sheetcontext>div').css("display","none")
        $('.sheetcontext>div')[$(this).parent().index()].style.display='block'
    })
})
