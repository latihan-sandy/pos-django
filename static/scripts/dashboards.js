$(document).ready(function () {

    var d = new Date();
    var n = d.getFullYear();


    var barChart = function (container, purchase, sale) {
        Highcharts.chart(container, {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Monthly Sale Vs Purchase'
            },
            xAxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            },
            yAxis: {
                title: {
                    text: 'Total Cost'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: false
                }
            },
            series: [{
                name: 'Purchase',
                data: purchase
            }, {
                name: 'Sale',
                data: sale
            }]
        });
    }

    var pieChart = function (data, title, container) {

        let items = new Array();

        data.forEach(function (row) {
            items.push({
                "name": row.name,
                "y": parseInt(row.total)
            });
        });

        let year = n;

        Highcharts.chart(container, {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie',
            },
            title: {
                text: title
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    },
                    showInLegend: true
                }
            },
            series: [{
                name: 'Product',
                colorByPoint: true,
                data: items
            }]
        });
    }

    var loadData = function () {
       
         $.ajaxSetup({
             headers: {
                'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val(),
             }
         });
        $.post("/dashboard/api", function (result) {

            $(".count-product").text(result.product);
            $(".count-brand").text(result.brand);
            $(".count-supplier").text(result.supplier);
            $(".count-customer").text(result.customer);

            pieChart(result.sale, "Sale By Product", "pie-chart1");
            pieChart(result.purchase, "Purchase By Product", "pie-chart2");
            barChart("bar-chart", result.chartPurchase, result.chartSale);

            $("#loader").addClass("hidden");
        });
    }


    loadData();

});