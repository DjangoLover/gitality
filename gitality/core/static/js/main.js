$(document).ready(function() {
    var $projform = $('.create-proj-form');
    $('#top-menu').dropdown();
    $('#js-cancel-proj').on('click', function() {
        $projform.find("input[type=text]").val("");
    });
    $('#js-create-proj').on('click', function() {
        $projform.submit();
    });
});
