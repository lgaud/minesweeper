import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.db.models import Avg, Min


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
    
    grid = game.get_display_grid()
    # add clear logic
    context = {
        'game_id': game_id,
        'state': game.state,
        'grid': grid,
    }
    return render(request, 'game/game.html', context)
    
def reveal(request, game_id):
    x = int(request.POST['x'])
    y = int(request.POST['y'])
    game = get_object_or_404(Game, pk=game_id)
    result = game.reveal_cell(x, y)
    return JsonResponse(result)
    
def toggle_marking(request, game_id):
    x = int(request.POST['x'])
    y = int(request.POST['y'])
    game = get_object_or_404(Game, pk=game_id)
    result = game.toggle_cell_marking(x, y)
    return JsonResponse({"state": result})
    
def stats(request):
    total_games_won = Game.objects.filter(state="W").count()
    total_games_lost = Game.objects.filter(state="L").count()
    total_games_completed = total_games_won + total_games_lost

    unlucky = Game.objects.filter(state="L",  num_moves=1).count()
    context = {
        'total_games_completed': total_games_completed,
        'total_games_won': total_games_won,
        'total_games_lost': total_games_lost,
        'unlucky': unlucky
    }
    return render(request, 'game/stats.html', context)