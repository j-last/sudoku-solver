
NUMS = set(["1","2","3","4","5","6","7","8","9"])

# Helper methods
def get_row(cells, y:int) -> set:
    """Returns a set of all values in a row of the grid

    Args:
        cells: The grid of cells to check.
        y: The row to check get the values for
    """
    row = set()
    for cell in cells[y]:
        row.add(cell.get())
    return row

def get_col(cells, x:int) -> set:
    """Returns a set of all values in a column of the grid

    Args:
        cells: The grid of cells to check.
        y: The column to check get the values for
    """
    col = set()
    for y in range(9):
        col.add(cells[y][x].get())
    return col

def get_box(cells, x:int, y:int) -> set:
    """Returns a set of all values in a 3x3 box of the grid of cells

    Args:
        cells: The grid of cells to check.
        x: The x-coordinate of any cell in the box being inspected.
        y: The y-coordinate of any cell in the box being inspected.
    """
    box = set()
    # Gets the x and y coordinates of the top left cell of the 3x3 box
    y = y - y%3
    x = x - x%3
    for i in range(3):
        for j in range(3):
            box.add(cells[y+i][x+j].get())
    return box

def get_possible_digits(grid:list[list[str]], x:int, y:int) -> set:
    """Returns all possible values that a cell can take.

    Args:
        grid: The grid to check.
        x: The x-coordinate of the cell.
        y: The y-coordinate of the cell.
    """
    return NUMS - get_row(grid, y) - get_col(grid, x) - get_box(grid, x, y)