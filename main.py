import tkinter as tk
from tools import validate_entry

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
        self.create_grid() # fills self.cells

    """Creates a blank sudoku grid, adding the entry boxes to the 2D array self.cells
    """
    def create_grid(self):
        valid = self.root.register(validate_entry)
        for y in range(9):
            # Allows the rows and colums to grow in size
            self.grid_frame.rowconfigure(y, weight=1)
            self.grid_frame.columnconfigure(y, weight=1)
            row = []
            for x in range(9):
                # Creates a cell that you can enter text into
                cell = tk.Entry(self.grid_frame, justify="center", 
                                font=("Arial", 20), bd=1, insertontime=0,
                                validate="key", validatecommand=(valid, "%P"))

                # Adds the cell to the grid, visually dividing them into 9 3x3 squares
                left = 1 if x % 3 == 0 else 0
                top = 1 if y % 3 == 0 else 0
                cell.grid(row=y, column=x, sticky="nsew", padx=(left, 0), pady=(top, 0))

                # Allows for the arrows to move between cells
                cell.bind("<Up>", lambda e, x=x, y=y: self.move_focus(e, x, y))
                cell.bind("<Down>", lambda e, x=x, y=y: self.move_focus(e, x, y))
                cell.bind("<Left>", lambda e, x=x, y=y: self.move_focus(e, x, y))
                cell.bind("<Right>", lambda e, x=x, y=y: self.move_focus(e, x, y))

                # Allows for highlighting of the currently selected cell
                cell.bind("<FocusIn>", lambda e: e.widget.config(bg="#ffaaaa"))
                cell.bind("<FocusOut>", lambda e: e.widget.config(bg="white"))

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


if __name__ == "__main__":
    root = tk.Tk()
    app = Grid(root)
    root.mainloop()