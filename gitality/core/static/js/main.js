$(document).ready(function() {
    $('#top-menu').dropdown();
    $('#js-cancel-proj').on('click', function() {
        $('.create-proj-form').find("input[type=text]").val("");
    });
});
