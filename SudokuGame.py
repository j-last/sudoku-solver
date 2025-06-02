import tkinter as tk
from Solvers import backtracking_solver, simulated_annealing_solver

class SudokuGame:
    def __init__(self, root:tk.Tk):
        """Initialises the sudoku grid, 

        Args:
            root (tk.Tk): The root for the tkinter window.
        """
        # Initialises the window
        self.__root = root
        self.__root.geometry("600x600")
        self.__root.title("Sudoku")

        # Initialises the frame the sudoku grid will be in and places it on the window
        self.__grid_frame = tk.Frame(root, bg="#000000")
        self.__grid_frame.pack(expand=True, fill="both")

        self.__grid = []
        self.create_grid() # sets up the cells of the grid and adds them to self.grid
        self.load_puzzle("puzzle1.txt") # places the initial digits in the grid, ensuring they cannot be changed
        self.change_focus(4, 4) # Initially highlights the middle box


    def create_grid(self):
        """Creates the cells of the grid, and adds them to the window and self.grid. 
        """
        valid = self.__root.register(lambda value: len(value) <= 1 and value in "123456789")
        for y in range(9):
            # Allows the rows and colums to grow in size
            self.__grid_frame.rowconfigure(y, weight=1)
            self.__grid_frame.columnconfigure(y, weight=1)
            row = []
            for x in range(9):
                # Creates a cell that you can enter text into
                cell = tk.Entry(self.__grid_frame, justify="center", 
                                font=("Arial", 20), insertontime=0,
                                validate="key", validatecommand=(valid, "%P"), 
                                relief="raised")
                # Adds the cell to the grid, visually dividing them into 9 3x3 squares using padding
                left = 2 if x % 3 == 0 else 0
                top = 2 if y % 3 == 0 else 0
                cell.grid(row=y, column=x, sticky="nsew", padx=(left, 0), pady=(top, 0))
                
                # Allows for the arrows to move between grid
                cell.bind("<Up>", lambda e, x=x, y=y: self.change_focus(x, y-1))
                cell.bind("<Down>", lambda e, x=x, y=y: self.change_focus(x, y+1))
                cell.bind("<Left>", lambda e, x=x, y=y: self.change_focus(x-1, y))
                cell.bind("<Right>", lambda e, x=x, y=y: self.change_focus(x+1, y))
                cell.bind("b", lambda e: backtracking_solver(self, 2))
                cell.bind("s", lambda e: simulated_annealing_solver(self, 2))
                row.append(cell)

            self.__grid.append(row)

    
    def change_focus(self, new_x:int, new_y:int):
        """Changes the highlight and cursor to a new cell in the grid.
        Highlights all other cells with the same value (apart from blank ones)
        and lightly highlights the current row + column.

        Args:
            new_x (int): The x-coordinate of the new cell.
            new_y (int): The y-coordinate of the new cell.
        """
        if not (0 <= new_x < 9 and 0 <= new_y < 9):
            return
        for y in range(9):
            for x in range(9):
                highlighted = False
                if x == new_x or y == new_y:
                    self.__grid[y][x].configure(background="#ffd59e")
                    highlighted = True
                if self.get_cell_value(new_x, new_y) != "" and self.get_cell_value(x, y) == self.get_cell_value(new_x, new_y):
                    self.__grid[y][x].configure(background="#a9e5e5")
                    highlighted = True
                if not highlighted:
                    self.__grid[y][x].configure(background="#fff9d8")
        self.__grid[new_y][new_x].configure(background="#b2ebe0")
        self.__grid[new_y][new_x].focus_set()


    def load_puzzle(self, filename:str):
        """Loads a sudoku grid from a file - ensuring the given numbers cannot be changed.

        Args:
            filename (str): The filename of the sudoku grid.
        """
        valid = self.__root.register(lambda value: False) # Input validation that always returns false (values cannot be changed).
        with open(filename) as puzzle:
            for y, row in enumerate(puzzle):
                for x, digit in enumerate(row):
                    if digit in "123456789":
                        # Adds the digit from the file to the grid
                        self.__grid[y][x].insert(0, digit)
                        # Overwrites the previous input validation with the new one (and makes the font bold).
                        self.__grid[y][x].configure(validatecommand=(valid, "%P"), font=("Arial", 20, "bold"))
    

    def get_cell_value(self, x:int, y:int) -> str:
        """Returns the value of a given cell in the grid.

        Args:
            x (int): The x-coord of the cell.
            y (int): The y-coord of the cell.
        """
        return self.__grid[y][x].get()
    

    def is_editable(self, x:int, y:int) -> bool:
        """Returns True if the cell specified is editable, False otherwise.
        If x or y are not 0-8 (inclusive) then False is also returned.

        Args:
            x (int): The x-coord of the cell.
            y (int): The y-coord of the cell.
        """
        if not (0 <= x < 9 and 0 <= y < 9):
            return False
        return self.__grid[y][x]["font"][-4:] != "bold"


    def change_cell(self, x:int, y:int, new_value:str):
        """Changes the cell to position (x, y) in the sudoku grid to a new value.
        Also sets the cursor/highlight to this cell and updates the window to display this change immediately.

        Args:
            x (int): The x-coord of the cell to change.
            y (int): The y-coord of the cell to change.
            new_value (str): The value to change it to.
        """
        self.__grid[y][x].delete(0, tk.END)
        self.__grid[y][x].insert(0, new_value)
        self.change_focus(x, y)
        
    
    def update_screen(self):
        self.__root.update()

    

    def get_row(self, y:int) -> set[str]:
        """Returns all values in a given row of the grid.

        Args:
            y (int): The y-coord of the row to get the values for.
        """
        values = set()
        for cell in self.__grid[y]:
            values.add(cell.get())
        return values
    

    def get_col(self, x:int) -> set[str]:
        """Returns all values in a given column of the grid.

        Args:
            x (int): The x-coord of the column to get the values for.
        """
        values = set()
        for y in range(9):
            values.add(self.__grid[y][x].get())
        return values
    

    def get_3x3box(self, x:int, y:int) -> set[str]:
        """Returns all values in the same 3x3 box in the grid as the cell given.

        Args:
            x (int): The x-coord of the cell.
            y (int): The y-coord of the cell.
        """
        box = set()
        # Gets the x and y coordinates of the top left cell of the 3x3 box
        y = y - y%3
        x = x - x%3
        for i in range(3):
            for j in range(3):
                box.add(self.__grid[y+i][x+j].get())
        return box
    

    def get_possible_digits(self, x:int, y:int) -> set[str]:
        """Returns all possible values a cell can take.

        Args:
            x (int): The x-coord of the cell.
            y (int): The y-coord of the cell.
        """
        NUMS = set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        return NUMS - self.get_col(x) - self.get_row(y) - self.get_3x3box(x, y)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGame(root)
    root.mainloop()
