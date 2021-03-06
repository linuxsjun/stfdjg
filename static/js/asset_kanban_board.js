$(function () {
    init('这是一个初始模块');
});

function init(obj){
    // 激活sideMenu
    var navitem = $('.nav-link');
    navitem.removeClass('active');
    $('#menu02').addClass('active');
    $('#menu020101').addClass('active');

    $.get('/asset_kanban_board/',
        {
            act: 'pi'
        },
        function (data) {
            if(data.code === 0) {
                var t = new Array();
                var n = new Array();
                $.each(data.data, function (i, item) {
                    t[i] = item['disname'];
                    n[i] = item['count'];
                });
                var chartCanvas = $("#chartContainer");
                var chartCanvas = new Chart(chartCanvas, {
                    type: 'pie',
                    data: {
                        labels: t,
                        datasets: [{
                            label: 'ssss',
                            data: n,
                            backgroundColor: [
                                'rgba(200, 200, 200, 0.6)',
                                'rgba(75, 192, 75, 0.6)',
                                'rgba(255, 159, 64, 0.6)',
                                'rgba(255, 2, 132, 0.6)'
                            ]
                        }]
                    }
                });
            }
        }
    );

    $.get('/asset_kanban_board/',
        {
            act: 'y_num'
        },
        function (data) {
            if(data.code === 0){
                var t = new Array();
                var n = new Array();
                $.each(data.data,function (i,item) {
                    t[i] = item['year'];
                    n[i] = item['count'];
                });
                var secendCanvas = $("#secend");
                var secendCanvas = new Chart(secendCanvas, {
                    type: 'bar',
                    data: {
                        labels: t,
                        datasets: [{
                            label: '数量',
                            data: n,
                            backgroundColor: [
                                'rgba(255, 2, 132, 0.6)',
                                'rgba(54, 162, 235, 0.6)',
                                'rgba(255, 159, 64, 0.6)',
                                'rgba(255, 99, 132, 0.6)',
                                'rgba(54, 162, 235, 0.6)',
                                'rgba(255, 206, 86, 0.6)',
                                'rgba(75, 192, 192, 0.6)',
                                'rgba(153, 102, 255, 0.6)',
                                'rgba(255, 159, 64, 0.6)',
                                'rgba(255, 99, 132, 0.6)',
                                'rgba(54, 162, 235, 0.6)',
                                'rgba(255, 206, 86, 0.6)',
                                'rgba(75, 192, 192, 0.6)',
                                'rgba(153, 102, 255, 0.6)'
                            ]
                        }]
                    }
                });
            }
        }
    );

    $.get('/asset_kanban_board/',
        {
            act: 'y_price'
        },
        function (data) {
            if(data.code === 0){
                var t = new Array();
                var n = new Array();
                $.each(data.data,function (i,item) {
                    t[i] = item['year'];
                    n[i] = item['price'];
                });
                var popCanvas = $("#popChart");
                var barChart = new Chart(popCanvas, {
                    type: 'line',
                    data: {
                        labels: t,
                        datasets: [{
                            label: '金额',
                            data: n,
                            color: 'rgba(54, 162, 235, 0.6)',
                            fill: false
                        }]
                    }
                });
            }
        }
    );

    $.get('/asset_kanban_board/',
        {
            act: 'dep_num'
        },
        function (data) {
            if(data.code === 0){
                var t = new Array();
                var n = new Array();
                var m = new Array();
                $.each(data.data,function (i,item) {
                    t[i] = item['name'];
                    n[i] = item['num'];
                    m[i] = item['picre'];
                });
                var popCanvas = $("#depassetbar");
                var barChart = new Chart(popCanvas, {
                    type: 'bar',
                    data: {
                        labels: t,
                        datasets: [
                            {
                            label: '数量',
                            data: n,
                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                            fill: false
                        }
                        // , {
                        //     label: '金额',
                        //     data: m,
                        //     backgroundColor: 'rgba(255, 99, 132, 0.6)',
                        //     fill: false,
                        //     type: 'bar'
                        // }
                        ]
                    }
                });
            }
        }
    );
}