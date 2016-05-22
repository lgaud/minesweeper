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
                if(response.hit) {
                    alert("You lose!")
                }
                else {
                    for(var i = 0; i < response.cleared_cells.length; i++) {
                        cell = response.cleared_cells[i]
                        display_cell = $("button[name='" + cell.x + "." + cell.y + "']")
                        display_cell.prop("disabled", true)
                        if(cell.adjacent_mines > 0) {
                            display_cell.text(cell.adjacent_mines);
                        }
                    }
                }
            }
        });
    }
    
    return ms;
}(jQuery));