from time import sleep
#from SudokuGame import SudokuGame
from random import random, randint, choice
from math import exp

def backtracking_solver(grid, speed:int):
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


def simulated_annealing_solver(grid, speed:int):
    """Solves the sudoku using simulated annealing, displaying the swaps made to the user.

    Args:
        grid (SudokuGame): The game of sudoku to be solved.
        speed (int): The speed at which the algorithm is ran.
    """
    NUMS = set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    iters = 0
    temp = 3
    MIN_TEMP = 0.1
    DECREASE_FACTOR = 0.999999
    for y in range(9):
        for x in range(9):
            if grid.get_cell_value(x, y) == "":
                grid.change_cell(x, y, choice(list(NUMS - grid.get_3x3box(x, y))))

    prev_score = get_score(grid)
    while temp > MIN_TEMP:
        # Selects any two editable cells in the same 3x3 box
        valid = False
        while not valid:
            x1, y1 = randint(0, 8), randint(0, 8)
            x2, y2 = randint(x1-x1%3, x1-x1%3+2), randint(y1-y1%3, y1-y1%3+2)
            valid = grid.is_editable(x1, y1) and grid.is_editable(x2, y2) and (x1, y1) != (x2, y2)

        val1, val2 = grid.get_cell_value(x1, y1), grid.get_cell_value(x2, y2)
        grid.change_cell(x1, y1, val2)
        grid.change_cell(x2, y2, val1)

        new_score = get_score(grid)

        if new_score < prev_score:
            grid.update_screen()
            prev_score = new_score
        elif exp(new_score - prev_score)/temp < random():
            grid.update_screen()
            prev_score = new_score
        else:
            grid.change_cell(x1, y1, val1)
            grid.change_cell(x2, y2, val2)
        if prev_score == 0:
            print(iters)
            break
        iters += 1
        temp *= DECREASE_FACTOR


def get_score(grid) -> int:
    score = 0
    for i in range(9):
        score += 9 - len(grid.get_row(i))
        score += 9 - len(grid.get_col(i))
    return score
        
        

        
        


