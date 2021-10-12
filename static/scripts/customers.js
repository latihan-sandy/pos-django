$(document).ready(function() {


    let dataTableColumns = [{
        name: 'customer_name',
        data: 'customer_name'
    }, {
        name: 'customer_phone',
        data: 'customer_phone'
    }, {
        name: 'customer_email',
        data: 'customer_email'
    }, {
        name: 'key_id',
        data: 'action',
        "orderable": false
    }, ];


    dataTableInit({
        "container": "#table-data",
        "route": "/customers/datatable",
        "columns": dataTableColumns
    });

});