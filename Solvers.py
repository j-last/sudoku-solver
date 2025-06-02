from time import sleep
from SudokuGame import SudokuGame
from random import random

def backtracking_solver(grid:SudokuGame, speed:int):
    """Solves the sudoku using backtracking, displaying the steps to the user.

    Args:
        grid (SudokuGame): The game to solve.
        speed (int): The speed to solve it at (slow 0 < speed <= 10 quick)
    """
    def solve(x:int, y:int):
        """Recursively solves the sudoku using backtracking.

        Args:
            x (int): The x-coord of the current cell.
            y (int): The y-coord of the current cell.

        Returns:
            bool: True if the sudoku is solvable, false otherwise.
        """
        nonlocal delay
        # Base case: The end of the grid reached.
        if x == 0 and y == 9: return True

        # Grid position already filled (move to next cell)
        if grid.get_cell(x, y) != "":
            return solve((x+1)%9, y+(x+1)//9)
        
        # Recurses with each digit that can go in the current cell
        for num in grid.get_possible_digits(x, y):
            # Changes the cell and updates the screen, with a delay so you can see each number being tried
            grid.change_cell(x, y, num)
            sleep(delay)
            if solve((x+1)%9, y+(x+1)//9): return True
        grid.change_cell(x, y, "")
        sleep(delay)
        return False
    assert 0 < speed <= 10
    delay = 0.1 / speed
    solve(0, 0)



