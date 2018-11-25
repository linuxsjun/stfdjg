window.onload = function() {
    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        title: {
            text: ""
        },
        data: [{
            type: "pie",
            startAngle: 45,
            yValueFormatString: "0",
            indexLabel: "{label} {y}",
            dataPoints: [
                {y: 321, label: "闲置"},
                {y: 506, label: "在用"},
                {y: 6, label: "维修"},
                {y: 77, label: "报废"}
            ]
        }]
    });
    var datachart = [{y: 22, label: "闲置"},{y: 22, label: "在用"},{y: 22, label: "维修"},{y: 22, label: "报废"}];
    chart.options.data.dataPoints += datachart;
    // chart.options.title.text += ": Updated";
    chart.render();

    var linechart = new CanvasJS.Chart("secend", {
        animationEnabled: true,
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        title:{
            text: ""
        },
        axisY: {
            title: "数量"
        },
        data: [{
            type: "column",
            showInLegend: true,
            legendMarkerColor: "grey",
            legendText: "年份",
            dataPoints: [
                { y: 15, label: "2007" },
                { y: 18,  label: "2008" },
                { y: 62,  label: "2009" },
                { y: 26,  label: "2010" },
                { y: 66,  label: "2011" },
                { y: 99, label: "2012" },
                { y: 24,  label: "2013" },
                { y: 5,  label: "2014" },
                { y: 15,  label: "2015" },
                { y: 1,  label: "2016" },
                { y: 7,  label: "2017" },
                { y: 1,  label: "2018" }
            ]
        }]
    });
    linechart.render();

    var popCanvas = $("#popChart");
    var popCanvas = document.getElementById("popChart");
    var popCanvas = document.getElementById("popChart").getContext("2d");

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

$(document).ready(function () {

});