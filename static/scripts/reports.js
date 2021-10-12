$(document).ready(function() {

    $("body").on("click", ".btn-report-show", function(e) {
        e.preventDefault();
        let url = $(this).attr("data-href");
        let first_date = $("#first_date").val();
        let last_date = $("#last_date").val();
        $("#iframe-report").attr("src", url + "/" + first_date + "/" + last_date);
        $("#myModal").modal("show");
        return false;
    });

    $('.date-filter').datepicker({
        autoclose: true,
        clearBtn: true,
        format: 'yyyy-mm-dd'
    }).on('changeDate', function(ev) {
        let url = $("#iframe-report").attr("src");
        let prefix = url.split('/');
        let first_date = $("#first_date").val();
        let last_date = $("#last_date").val();
        let newPrefix = new Array();
        newPrefix.push(prefix[0]);
        newPrefix.push(first_date);
        newPrefix.push(last_date);
        let reportUrl = newPrefix.join("/");
        if (first_date && last_date) {
            $("#iframe-report").attr("src", reportUrl);
        }

    });

    $("#btn-print").click(function(e) {
        e.preventDefault();
        document.getElementById('iframe-report').contentWindow.print();
        return false;
    });

});