$(document).ready(function() {


    let dataTableColumns = [{
        name: 'brand_name',
        data: 'brand_name'
    }, {
        name: 'brand_description',
        data: 'brand_description',
        render: function(data, type, row, meta) {
            var notif = data.split(".");
            return notif[0];
        }
    }, {
        name: 'key_id',
        data: 'action',
        "orderable": false
    }, ];


    dataTableInit({
        "container": "#table-data",
        "route": "/brands/datatable",
        "columns": dataTableColumns
    });

});