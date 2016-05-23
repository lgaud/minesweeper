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
                    handle_hit(x, y, response.mine_locations); 
                    self.end_game(false);
                }
                else {
                    handle_clear(response.cleared_cells)
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
        // cycle between flagged, question, and unmarked
        var game_id = $("#game_id").val();
        var csrf = $("[name='csrfmiddlewaretoken']").val();
        $.ajax({
            url: "/game/" + game_id + "/mark/",
            method: "POST",
            data: {x: x, y: y, csrfmiddlewaretoken: csrf},
            success: function(response) {
                handle_mark_cell(x, y, response.state);
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
    
    function handle_hit(x, y, mine_locations) {
        for(var i = 0; i < mine_locations.length; i++) {
            var mine = mine_locations[i];
            var cell = $("button[name='" + mine.x + "." + mine.y + "']")
            cell.html('<span class="glyphicon glyphicon-fire" aria-hidden="true"></span>')
            if(mine.x == x && mine.y == y) {
                cell.removeClass("btn-primary")
                cell.addClass("btn-danger")
            }
        }
    }
    
    function handle_clear(cleared_cells) {
        for(var i = 0; i < cleared_cells.length; i++) {
            var cell = cleared_cells[i]
            var display_cell = $("button[name='" + cell.x + "." + cell.y + "']")
            display_cell.prop("disabled", true)
            display_cell.addClass("disabled")
            if(cell.adjacent_mines > 0) {
                display_cell.text(cell.adjacent_mines);
            }
        }
    }
    
    function handle_mark_cell(x, y, state) {
            var cell = $(".cell[name='" + x + "." + y + "']");
            if(state == "F") {
                cell.html('<span class="glyphicon glyphicon-flag" aria-hidden="true"></span>')
            }
            else if(state == "?") {
                cell.html('<span class="glyphicon glyphicon-question-sign" aria-hidden="true"></span>');
            }
            else if(state == "H") {
                cell.html("");
            }
    }
    
    return ms;
}(jQuery));