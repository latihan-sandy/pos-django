$(document).ready(function() {


    let dataTableColumns = [{
        name: 'group_name',
        data: 'group_name'
    }, {
        name: 'key_id',
        data: 'action',
        "orderable": false
    }, ];


    dataTableInit({
        "container": "#table-data",
        "route": "/groups/datatable",
        "columns": dataTableColumns
    });

});