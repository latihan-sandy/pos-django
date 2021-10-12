$(document).ready(function() {


    let dataTableColumns = [{
        name: 'supplier_name',
        data: 'supplier_name'
    }, {
        name: 'supplier_phone',
        data: 'supplier_phone'
    }, {
        name: 'supplier_email',
        data: 'supplier_email'
    }, {
        name: 'key_id',
        data: 'action',
        "orderable": false
    }, ];


    dataTableInit({
        "container": "#table-data",
        "route": "/suppliers/datatable",
        "columns": dataTableColumns
    });

});