window.onload = function() {
    var chartCanvas = $("#chartContainer");
    // var chartCanvas = document.getElementById("chartContainer");
    // var chartCanvas = document.getElementById("chartContainer").getContext("2d");

    var schartCanvas = new Chart(chartCanvas, {
        type: 'pie',
        data: {
            labels: ["闲置(352)", "在用(505)", "维修(7)", "报废(76)"],
            datasets: [{
                // label: '',
                data: [362, 505, 7, 76],
                backgroundColor: [
                    'rgba(200, 200, 200, 0.6)',
                    'rgba(75, 192, 75, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
                    'rgba(255, 2, 132, 0.6)'
                ]
            }]
        }
    });

    var secendCanvas = $("#secend");
    // var secendCanvas = document.getElementById("secend");
    // var secendCanvas = document.getElementById("secend").getContext("2d");

    var secendCanvas = new Chart(secendCanvas, {
        type: 'bar',
        data: {
            labels: ["2007", "2008", "2009", "2010", "1011", "2012", "2013", "2014", "2015", "2016"],
            datasets: [{
                label: '年份',
                data: [15, 18, 62, 26, 66, 72, 24, 5, 15, 1],
                backgroundColor: [
                    'rgba(255, 2, 132, 0.6)',
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

    var popCanvas = $("#popChart");
    // var popCanvas = document.getElementById("popChart");
    // var popCanvas = document.getElementById("popChart").getContext("2d");

    var barChart = new Chart(popCanvas, {
        type: 'bar',
        data: {
            labels: ["China", "India", "United", "Indonesia", "Brazil", "Pakistan", "Nigeria", "Bangladesh", "Russia", "Japan"],
            datasets: [{
                label: 'Pop',
                data: [137971, 128911, 325791, 26039, 20391, 204861, 12261, 157828, 14219, 12698],
                backgroundColor: [
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
};

$(function () {

});