$(function () {
    init('页面初始化');
});

function init(obj) {
    // console.log(obj);

    // 激活sideMenu
    var navitem = $('nav').find('.nav-link');
    navitem.removeClass('active');
    $('#menu02').addClass('active');
    $('#menu020302').addClass('active');
}