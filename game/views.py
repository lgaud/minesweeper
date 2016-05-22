import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse

from .models import Game


# Create your views here.
def index(request):
    return render(request, 'game/index.html')

def create_game(request):
    rows = int(request.POST['rows'])
    columns = int(request.POST['columns'])
    mines = int(request.POST['mines'])
    game = Game(x_cells=columns, y_cells=rows, num_mines=mines)
    game.create_game()
    return redirect('game', game_id=game.id)
    
def game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    # add clear logic
    context = {
        'x_cells': game.x_cells,
        'y_cells': game.y_cells,
        'x_range': range(game.x_cells),
        'y_range': range(game.y_cells)
    }
    return render(request, 'game/game.html', context)
    
def reveal(request, game_id):
    x = int(request.POST['x'])
    y = int(request.POST['y'])
    game = get_object_or_404(Game, pk=game_id)
    result = game.reveal_cell(x, y)
    data = json.dumps(result)
    return HttpResponse(data)
    