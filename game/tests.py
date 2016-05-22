from django.test import TestCase
from .models import Game
# Create your tests here.
# https://docs.djangoproject.com/en/1.9/intro/tutorial05/

class GameCreatonTests(TestCase):
    def test_create_2x2_grid_top_left(self):
        game = Game(x_cells=2, y_cells=2, num_mines=1)
        mines = [(0, 0)]
        grid = game.create_grid(mines)
        
        self.assertEqual(grid[0][0], 0)
        self.assertEqual(grid[0][1], 1)
        self.assertEqual(grid[1][0], 1)
        self.assertEqual(grid[1][1], 1)

    def test_create_2x2_grid_top_right(self):
        game = Game(x_cells=2, y_cells=2, num_mines=1)
        mines = [(1, 0)]
        grid = game.create_grid(mines)
        
        self.assertEqual(grid[0][0], 1)
        self.assertEqual(grid[0][1], 1)
        self.assertEqual(grid[1][0], 0)
        self.assertEqual(grid[1][1], 1)
    
    def test_create_2x2_grid_bottom_left(self):
        game = Game(x_cells=2, y_cells=2, num_mines=1)
        mines = [(0, 1)]
        grid = game.create_grid(mines)
        
        self.assertEqual(grid[0][0], 1)
        self.assertEqual(grid[0][1], 0)
        self.assertEqual(grid[1][0], 1)
        self.assertEqual(grid[1][1], 1)
        
    def test_create_wide_grid(self):
        game = Game(x_cells=5, y_cells=3, num_mines=1)
        mines = [(4, 2)]
        grid = game.create_grid(mines)
        self.assertEqual(grid[4][2], 0)
        self.assertEqual(grid[3][1], 1)
    
    def test_create_tall_grid(self):
        game = Game(x_cells=3, y_cells=5, num_mines=1)
        mines = [(2, 4)]
        grid = game.create_grid(mines)
        self.assertEqual(grid[2][4], 0)
        self.assertEqual(grid[1][3], 1)
        
    def test_create_mine_one_option(self):
        mines = [(0,1)]
        game = Game(x_cells=1, y_cells=2, num_mines=1)
        game.add_mine(mines)
        
        self.assertEqual(len(mines), 2)
        self.assertEqual(mines, [(0,1), (0,0)])
        
    def test_create_mines(self):
        mines = []
        
        game = Game(x_cells=2, y_cells=2, num_mines=3)
        for i in range(0, 3):
            game.add_mine(mines)
            
        self.assertEqual(len(mines), 3)
        
    def test_create_game(self):
        game = Game(x_cells=5, y_cells=5, num_mines=3)
        mines = [(0, 0), (0, 1), (0, 2)]
        
        game.create_game(mines)
        
        self.assertEqual(len(Game.objects.all()),1)
        g = Game.objects.get(id=1)
        self.assertEqual(len(g.cell_set.all()), 25)
        top_left = g.cell_set.get(x_loc=0, y_loc=0)
        self.assertEqual(top_left.has_mine, True)
        adjacent = g.cell_set.get(x_loc=1, y_loc=0)
        self.assertEqual(adjacent.has_mine, False)
        self.assertEqual(adjacent.num_adjacent_mines, 2)

        
    def test_reveal_cell_hit(self):
        game = Game(x_cells=3, y_cells=3, num_mines=3)
        mines = [(0, 0), (0, 1), (0, 2)]
        game.create_game(mines)
        
        g = Game.objects.get(id=1)
        result = g.reveal_cell(0, 0)
        self.assertEqual(result["hit"], True)
        
    def test_reveal_cell_adjacentmine(self):
        game = Game(x_cells=3, y_cells=3, num_mines=3)
        mines = [(0, 0), (0, 1), (0, 2)]
        game.create_game(mines)
        
        g = Game.objects.get(id=1)
        result = g.reveal_cell(1, 1)
        self.assertEqual(result["hit"], False)
        self.assertEqual(result["cleared_cells"], [{'x': 1, 'y': 1, 'adjacent_mines': 3}])
        
    def test_reveal_cell_clear(self):
        game = Game(x_cells=3, y_cells=3, num_mines=3)
        mines = [(0, 0), (0, 1), (0, 2)]
        game.create_game(mines)
        
        g = Game.objects.get(id=1)
        result = g.reveal_cell(2, 0)
        self.assertEqual(result["hit"], False)
        self.assertEqual(result["cleared_cells"], 
            [{'x': 1, 'y': 0, 'adjacent_mines': 2}, 
            {'x': 1, 'y': 1, 'adjacent_mines': 3},
            {'x': 1, 'y': 2, 'adjacent_mines': 2},
            {'x': 2, 'y': 0, 'adjacent_mines': 0},
            {'x': 2, 'y': 1, 'adjacent_mines': 0},
            {'x': 2, 'y': 2, 'adjacent_mines': 0}])
     