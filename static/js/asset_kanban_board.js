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
                {y: 312, label: "闲置"},
                {y: 506, label: "在用"},
                {y: 6, label: "维修"},
                {y: 77, label: "报废"}
            ]
        }]
    });
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
};

$(document).ready(function () {

});