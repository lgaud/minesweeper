var minesweeper = (function($) {
    var ms = {};
    
    ms.reveal_cell = function(x, y) {
        game_id = $("#game_id").val();
        csrf = $("[name='csrfmiddlewaretoken']").val();
        $.ajax({
            url: "/game/" + game_id + "/reveal/",
            method: "POST",
            data: {x: x, y: y, csrfmiddlewaretoken: csrf},
            success: function(response) {
                alert(response);
            }
        });
    }
    
    return ms;
}(jQuery));