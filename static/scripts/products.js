$(document).ready(function () {


    let dataTableColumns = [{
        name: 'product_sku',
        data: 'product_sku'
    }, {
        name: 'product_name',
        data: 'product_name'
    }, 
    {
        name: 'product_stock',
        data: 'product_stock'
    },
    {
        name: 'key_id',
        data: 'action',
        "orderable": false
    },];

    if ($("#table-data").length){
         dataTableInit({
             "container": "#table-data",
             "route": "/products/datatable",
             "columns": dataTableColumns
         });
    }

   

    var calcPriceSale = function () {
        let purchase = parseFloat($("#id_price_purchase").val());
        let profit = parseFloat($("#id_price_profit").val());
        let prc = parseFloat(profit / 100);
        let cost = purchase * prc;
        let priceSale = purchase + cost;
        $("#id_price_sales").val(priceSale || purchase);
    }

    $('#id_price_purchase').keyup(function () {
        calcPriceSale();
    });

    $('#id_price_profit').keyup(function () {
        calcPriceSale();
    });

    $("#form-submit select").addClass("form-control");
    $("#form-submit select").select2({
         theme: "bootstrap",
    });

});