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
     