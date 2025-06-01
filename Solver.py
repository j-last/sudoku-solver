
NUMS = set(["1","2","3","4","5","6","7","8","9"])

# Helper methods
def get_row(grid:list[list[str]], y:int) -> set:
    """Returns a set of all values in a row of the grid

    Args:
        grid: The grid to check.
        y: The row to check get the values for
    """
    return set(grid[y])

def get_col(grid:list[list[str]], x:int) -> set:
    """Returns a set of all values in a column of the grid

    Args:
        grid: The grid to check.
        y: The column to check get the values for
    """
    col = set()
    for y in range(9):
        col.add(grid[y][x])
    return col

def get_box(grid:list[list[str]], x:int, y:int) -> set:
    """Returns a set of all values in a 3x3 box of the grid

    Args:
        grid: The grid to check.
        x: The x-coordinate of any cell in the box being inspected.
        y: The y-coordinate of any cell in the box being inspected.
    """
    box = set()
    # Gets the x and y coordinates of the top left cell of the 3x3 box
    y = y - y%3
    x = x - x%3
    for i in range(3):
        for j in range(3):
            box.add(grid[y+i][x+j])
    return box

def print_grid(grid:list[list[str]]):
    """Prints the grid in a more readable manner.

    Args:
        grid: The grid to print
    """
    for row in grid:
        print(row)
    print()

def get_possible_digits(grid:list[list[str]], x:int, y:int) -> set:
    """Returns all possible values that a cell can take.

    Args:
        grid: The grid to check.
        x: The x-coordinate of the cell.
        y: The y-coordinate of the cell.
    """
    return NUMS - get_row(grid, y) - get_col(grid, x) - get_box(grid, x, y)


# Backtracking solver
def solve(initial_grid:list[list[str]]) -> list[list[str]]:
    """Solves the sudoku.

    Args:
        initial_grid: The sudoku grid to solve.

    Returns:
        grid: The solved sudoku grid.
    """
    def solve(grid, pos):
        # Base case: The end of the grid reached.
        if pos == 81: return grid

        # Grid position already filled (move to next cell)
        x, y = pos % 9, pos // 9
        if grid[y][x] != "":
            return solve(grid, pos+1)
        
        # Recurses with each digit that can
        for num in get_possible_digits(grid, x, y):
            grid[y][x] = num
            solved = solve(grid, pos+1)
            if solved:
                return grid
        grid[y][x] = ""
        return False
    return solve(initial_grid, 0)


# Load a puzzle from the file for testing.
my_grid = [["" for x in range(9)] for y in range(9)]
with open("puzzle1.txt") as puzzle:
    for y, row in enumerate(puzzle):
        for x, digit in enumerate(row):
            if digit in "123456789":
                my_grid[y][x] = digit
print_grid(my_grid)
print_grid(solve(my_grid))