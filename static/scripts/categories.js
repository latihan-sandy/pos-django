$(document).ready(function() {


    let dataTableColumns = [{
        name: 'category_name',
        data: 'category_name'
    }, {
        name: 'category_description',
        data: 'category_description',
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
        "route": "/categories/datatable",
        "columns": dataTableColumns
    });

});