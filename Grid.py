import tkinter as tk
from SolveHelpers import get_possible_digits
from time import sleep

class Grid:
    def __init__(self, root):
        # Initialises the window
        self.root = root
        self.root.geometry("600x600")
        self.root.title("Sudoku")

        # Initialises the frame the grid will be in and places it on the window
        self.grid_frame = tk.Frame(root, bg="#666666")
        self.grid_frame.pack(expand=True, fill="both")

        self.cells = []
        self.create_grid() # sets up the cells of the grid and adds them to self.cells
        self.initialise_grid() # places the initial digits in the grid, ensuring they cannot be changed

    """Creates a blank sudoku grid, adding the entry boxes to the 2D array self.cells
    """
    def create_grid(self):
        valid = self.root.register(lambda value: len(value) <= 1 and value in "123456789")
        for y in range(9):
            # Allows the rows and colums to grow in size
            self.grid_frame.rowconfigure(y, weight=1)
            self.grid_frame.columnconfigure(y, weight=1)
            row = []
            for x in range(9):
                # Creates a cell that you can enter text into
                cell = tk.Entry(self.grid_frame, justify="center", 
                                font=("Arial", 20), bd=1, insertontime=0,
                                validate="key", validatecommand=(valid, "%P"),
                                readonlybackground="white"
                                )
                # Adds the cell to the grid, visually dividing them into 9 3x3 squares
                left = 1 if x % 3 == 0 else 0
                top = 1 if y % 3 == 0 else 0
                cell.grid(row=y, column=x, sticky="nsew", padx=(left, 0), pady=(top, 0))

                # Allows for the arrows to move between cells
                cell.bind("<Up>", lambda e, x=x, y=y: self.move_focus(e, x, y))
                cell.bind("<Down>", lambda e, x=x, y=y: self.move_focus(e, x, y))
                cell.bind("<Left>", lambda e, x=x, y=y: self.move_focus(e, x, y))
                cell.bind("<Right>", lambda e, x=x, y=y: self.move_focus(e, x, y))
                cell.bind("s", lambda e: self.solve())
            
                # Allows for coloured highlighting of the cell currently in focus.
                cell.bind("<FocusIn>", lambda e: e.widget.config(bg="#ffaaaa"))
                cell.bind("<FocusOut>", lambda e: e.widget.config(bg="white"))

                # Disables highlighting of the cell

                row.append(cell)
            self.cells.append(row)
        self.cells[4][4].focus_set() # Initially highlights the middle box

    """Controls how the cell highlight is moved when the arrow keys are pressed.
    """
    def move_focus(self, event, x:int, y:int):
        key = event.keysym
        new_x = x
        new_y = y
        if key == "Up":
            new_y = max(0, y-1)
        elif key == "Down":
            new_y = min(8, y+1)
        elif key == "Left":
            new_x = max(0, x-1)
        elif key == "Right":
            new_x = min(8, x+1)
        self.cells[new_y][new_x].focus_set()


    def initialise_grid(self):
        valid = self.root.register(lambda value: False)
        with open("puzzle1.txt") as puzzle:
            for y, row in enumerate(puzzle):
                for x, digit in enumerate(row):
                    if digit in "123456789":
                        # Adds the digit from the file to the grid
                        self.cells[y][x].insert(0, digit)
                        # Changes the input validation to make this cell unchangeable (validation always returns False)
                        self.cells[y][x].configure(validatecommand=(valid, "%P"), font=("Arial", 20, "bold"))
    
    def solve(self):
        """Solves the sudoku.

        Returns:
            grid: The solved sudoku grid.
        """
        def solve(pos):
            # Base case: The end of the grid reached.
            if pos == 81: return True

            # Grid position already filled (move to next cell)
            x, y = pos % 9, pos // 9
            if self.cells[y][x].get() != "":
                return solve(pos+1)
            
            # Recurses with each digit that can
            possible = get_possible_digits(self.cells, x, y)
            for num in range(1, 10): # Looks cooler than just looping through the possible ones
                num = str(num)
                # Changes the cell and updates the screen, with a delay so you can see each number being tried
                self.cells[y][x].delete(0, tk.END)
                self.cells[y][x].insert(0, num)
                self.cells[y][x].focus_set()
                self.root.update()
                sleep(0.01)
                if num not in possible: continue
                if solve(pos+1): return True
            self.cells[y][x].focus_set()
            self.cells[y][x].delete(0, tk.END)
            self.root.update()
            sleep(0.01)
            return False
        return solve(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = Grid(root)
    root.mainloop()