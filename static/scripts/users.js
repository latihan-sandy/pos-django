$(document).ready(function() {


    let dataTableColumns = [{
        name: 'user_username',
        data: 'user_username'
    }, {
        name: 'user_email',
        data: 'user_email'
    }, {
        name: 'user_is_active',
        data: 'user_is_active',
        render: function(data, type, row, meta) {
            if (data) {
                return '<span class="label label-success">Enable</span></td>';
            } else {
                return '<span class="label label-danger">Disable</span></td>';
            }
        }
    }, {
        name: 'key_id',
        data: 'action',
        "orderable": false
    }, ];


    dataTableInit({
        "container": "#table-data",
        "route": "/users/datatable",
        "columns": dataTableColumns
    });

});