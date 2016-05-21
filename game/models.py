from django.db import models
import random


# Create your models here.
class Game(models.Model):
    x_cells = models.IntegerField(default=9)
    y_cells = models.IntegerField(default=9)
    num_mines = models.IntegerField(default=10)
    
    def create_game(self):
        if self.x_cells < 1 or self.y_cells < 1 or mines < 1:
            raise Exception('Values must be at least 1')
        if self.num_mines >= (self.x_cells * self.y_cells) / 2:
            raise Exception('Too many mines for grid')
            
        mines = []
        for i in range(0, self.num_mines):
            self.add_mine(mines)
            
        mines.sort()
        grid = self.create_grid(mines)
        self.save_grid(mines, grid)

        
    def create_grid(self, mines):
        grid = [[0 for x in range(self.x_cells)] for y in range(self.y_cells)]
        
        for m in mines:
            x = m[0]
            y = m[1]
            # increment count in surrounding cells
            # x-1
            if x > 0:
                if y > 0:
                    grid[x-1][y-1] += 1
                if y + 1 < self.y_cells:
                    grid[x-1][y+1] += 1
                grid[x-1][y] += 1
            #x
            if y > 0:
                grid[x][y-1] += 1
            if y + 1 < self.y_cells:
                grid[x][y+1] += 1
            
            #x + 1
            if x + 1 < self.x_cells:
                if y > 0:
                    grid[x+1][y-1] += 1
                if y + 1 < self.y_cells:
                    grid[x+1][y+1] += 1
                grid[x+1][y] += 1
               
        return grid

    def add_mine(self, mines):
        mine = (random.randint(0, self.x_cells-1), random.randint(0, self.y_cells - 1))
        if mine in mines:
            self.add_mine(mines)
        else:
            mines.append(mine)
    
    def save_grid(mines, grid):
        next_mine_index = 0
        for x, row in enumerate(grid):
            for y, col in enumerate(row):
                cell = Cell(x_loc=x, y_loc=y, num_adjacent_mines=grid[x][y])
                if(mines[next_mine_index] == (x, y)):
                    cell.has_mine = True
                    next_mine_index += 1
                cell.save()
    
class Cell(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    x_loc = models.IntegerField(default=0)
    y_loc = models.IntegerField(default=0)
    has_mine = models.BooleanField(default=False)
    num_adjacent_mines = models.IntegerField(default=0)
    
 
    