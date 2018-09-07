$(document).ready(function () {
    $('.sheet>div>div').css("display","none")
    $($('.sheet>div>div')[0]).css("display","block")
    $('.sheet>ul>li>a').click(function () {
        // $(this).css("background","#dddddd")
        // $(this).css("border","0px solid black")
        //
        // // alert($(this).index())
        // $(this).css("background","white")
        // $(this).css("border","1px solid black")
        // $(this).css("border-bottom","1px solid white")
        // $(this).css("border-Top","2px solid #cccc00")


        $('.sheetcontext>div').css("display","none")
        $('.sheetcontext>div')[$(this).parent().index()].style.display='block'
    })
})
