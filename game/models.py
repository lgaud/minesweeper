from django.db import models
import random


# Create your models here.
class Game(models.Model):
    x_cells = models.IntegerField(default=9)
    y_cells = models.IntegerField(default=9)
    num_mines = models.IntegerField(default=10)
    
    def get_display_grid(self):
        # Return a list of lists representing the display state of each cell
        # H - Hidden
        # F - Flag
        # ? - Question
        # M - Exposed Mine
        # [0-8] Clear, number of adjacent Mines
        cells = self.cell_set.all().order_by('x_loc', 'y_loc')
        # Index row, column for display purposes
        grid = [["H" for x in range(self.x_cells)] for y in range(self.y_cells)]
        for c in cells:
            if c.is_clear:
                if c.has_mine:
                    grid[c.y_loc][c.x_loc] = "M"
                else:
                    grid[c.y_loc][c.x_loc] = c.num_adjacent_mines
            if c.is_flagged:
                grid[c.y_loc][c.x_loc] = "F"
            if c.is_marked:
                grid[c.y_loc][c.x_loc] = "?"
        return grid
        
    
    def create_game(self, mines=None):
        if self.x_cells < 1 or self.y_cells < 1 or self.num_mines < 1:
            raise Exception('Values must be at least 1')
        if self.num_mines >= (self.x_cells * self.y_cells) / 2:
            raise Exception('Too many mines for grid')
        self.save()
        
        if mines == None:
            mines = self.create_mines()
            
        mines.sort()
        grid = self.create_grid(mines)
        self.save_grid(mines, grid)

        
    def create_grid(self, mines):
        grid = [[0 for y in range(self.y_cells)] for x in range(self.x_cells)]
        
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
            
    def create_mines(self):
        mines = []
        for i in range(0, self.num_mines):
            self.add_mine(mines)
        return mines
    
    def save_grid(self, mines, grid):
        next_mine_index = 0

        for x, row in enumerate(grid):
            for y, col in enumerate(row):
                cell = self.cell_set.create(x_loc=x, y_loc=y, num_adjacent_mines=grid[x][y])
                if(next_mine_index < self.num_mines and mines[next_mine_index] == (x, y)):
                    cell.has_mine = True
                    next_mine_index += 1
                
                cell.save()
                
    def reveal_cell(self, x, y):
        cell = self.cell_set.get(x_loc=x, y_loc=y)
        checked_cells = grid = [[False for y in range(self.y_cells)] for x in range(self.x_cells)]
        result = {}
        if cell.has_mine:
            result["hit"] = True
            c = self.cell_set.get(x_loc=x, y_loc=y)
            c.is_clear
            c.save()
        else:
            cleared_cells = self.check_cell(cell.x_loc, cell.y_loc, checked_cells)
            cleared_cells.sort(key=lambda k: k['y'])
            cleared_cells.sort(key=lambda k: k['x'])
            result["hit"] = False
            result["cleared_cells"] = cleared_cells
        
            for cleared in cleared_cells:
                c = self.cell_set.get(x_loc=cleared['x'], y_loc=cleared['y'])
                if not c.is_clear:
                    c.is_clear = True
                    c.save()
                    
        return result
    
    def toggle_cell_marking(self, x, y):
    # Cycle through: Flag, Mark, Nothing
        cell = self.cell_set.get(x_loc=x, y_loc=y)
        state = ""
        if not cell.is_clear:
            if cell.is_flagged:
                cell.is_flagged = False
                cell.is_marked = True
                state = "?"
            elif cell.is_marked:
                cell.is_flagged = False
                cell.is_marked = False
                state = "H"
            else:
                cell.is_flagged = True
                cell.is_marked = False
                state = "F"
            cell.save()
       
        return state
    
    
    def check_cell(self, x, y, checked_cells):
        # Return a list of adjacent cells with their adjacent mine count
        # Returns [] if this cell has a mine
        cleared_cells = []
        if checked_cells[x][y]:
            return cleared_cells
        checked_cells[x][y] = True
        cell = self.cell_set.get(x_loc=x, y_loc=y)
        if cell.has_mine:
            return cleared_cells
         
        cleared_cells.append({ 'x': cell.x_loc, 'y': cell.y_loc, 'adjacent_mines': cell.num_adjacent_mines })

        if cell.num_adjacent_mines == 0:
            # Check adjacent cells
            # x-1
            if x > 0:
                if y > 0:
                    cleared_cells.extend(self.check_cell(x-1, y-1, checked_cells))
                if y + 1 < self.y_cells:
                    cleared_cells.extend(self.check_cell(x-1, y+1, checked_cells))
                
                cleared_cells.extend(self.check_cell(x-1, y, checked_cells))
            #x
            if y > 0:
                cleared_cells.extend(self.check_cell(x, y-1, checked_cells))
            if y + 1 < self.y_cells:
                cleared_cells.extend(self.check_cell(x, y+1, checked_cells))
            
            #x + 1
            if x + 1 < self.x_cells:
                if y > 0:
                    cleared_cells.extend(self.check_cell(x+1, y-1, checked_cells))
                if y + 1 < self.y_cells:
                    cleared_cells.extend(self.check_cell(x+1, y+1, checked_cells))
                
                cleared_cells.extend(self.check_cell(x+1, y, checked_cells))
        
        return cleared_cells             
            
class Cell(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    x_loc = models.IntegerField(default=0)
    y_loc = models.IntegerField(default=0)
    has_mine = models.BooleanField(default=False)
    num_adjacent_mines = models.IntegerField(default=0)
    is_clear = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    is_marked = models.BooleanField(default=False)
    

    
 
    