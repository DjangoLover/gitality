$(document).ready(function() {
    $('#top-menu').dropdown();
    $('#js-create-proj').on('click', function() {
        $('.create-proj-form').submit();
    });
});
