var minesweeper = (function($) {
    var ms = {};
    
    ms.reveal_cell = function(x, y) {
        var self = this;
        var game_id = $("#game_id").val();
        var csrf = $("[name='csrfmiddlewaretoken']").val();
        $.ajax({
            url: "/game/" + game_id + "/reveal/",
            method: "POST",
            data: {x: x, y: y, csrfmiddlewaretoken: csrf},
            success: function(response) {
                if(response.hit) {
                    for(var i = 0; i < response.mine_locations.length; i++) {
                        var mine = response.mine_locations[i];
                        var cell = $("button[name='" + mine.x + "." + mine.y + "']")
                        cell.html('<span class="glyphicon glyphicon-fire" aria-hidden="true"></span>')
                        if(mine.x == x && mine.y == y) {
                            cell.removeClass("btn-primary")
                            cell.addClass("btn-danger")
                        }
                    }
                    self.end_game(false);
                    
                }
                else {
                    for(var i = 0; i < response.cleared_cells.length; i++) {
                        var cell = response.cleared_cells[i]
                        var display_cell = $("button[name='" + cell.x + "." + cell.y + "']")
                        display_cell.prop("disabled", true)
                        display_cell.addClass("disabled")
                        if(cell.adjacent_mines > 0) {
                            display_cell.text(cell.adjacent_mines);
                        }
                    }
                    if(response.is_win) {
                        self.end_game(true);
                    }
                }
            }
        });
    }
    
    ms.end_game = function(isWin) {
        // Disable all click events
        $(".cell").off();
        if(isWin) {
            $("#winMessage").show();
        }
        else {
            $("#loseMessage").show();
        }
    }
    
    ms.toggle_cell_marking = function(x, y) {
        var game_id = $("#game_id").val();
        var csrf = $("[name='csrfmiddlewaretoken']").val();
        $.ajax({
            url: "/game/" + game_id + "/mark/",
            method: "POST",
            data: {x: x, y: y, csrfmiddlewaretoken: csrf},
            success: function(response) {
                var cell = $(".cell[name='" + x + "." + y + "']");
                if(response.state == "F") {
                    cell.html('<span class="glyphicon glyphicon-flag" aria-hidden="true"></span>')
                }
                else if(response.state == "?") {
                    cell.html('<span class="glyphicon glyphicon-question-sign" aria-hidden="true"></span>');
                }
                else if(response.state == "H") {
                    cell.html("");
                }
            }
        });
    }
    
    ms.initialize = function() {
        var self = this;
        var cells = $(".cell");
        cells.click(function() {
            var contents = $(this).html();
            if(contents.trim() == "") {
                // Prevent clicking marked cells
                var values = $(this).attr("name").split(".");
                self.reveal_cell(values[0], values[1]);
            }
        });
        
        cells.contextmenu(function(e) {
            e.preventDefault();
            var values = $(this).attr("name").split(".");
            self.toggle_cell_marking(values[0], values[1]);
        });
    }
    
    return ms;
}(jQuery));