window.WwLogin({
"id" : "wx_reg",
"appid" : "ww74c5af840cdd5cb6",
"agentid" : "1000013",
"redirect_uri" :"http://127.0.0.1:8000/sign",
"state" : "{{ stat }}",
"href" : "",
});

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