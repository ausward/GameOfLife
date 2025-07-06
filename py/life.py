import random
import time
import copy # Used for deep copying cells for the next generation

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = False

    def is_alive(self):
        return self.alive

    def set_alive(self, state=True): # Default to True for convenience
        self.alive = state

    def set_dead(self):
        self.alive = False

# Define the letter patterns as a global dictionary, similar to your Go map
# These are 5x3 boolean arrays for each character
letters = {
    'S': [
        [True, True, True],
        [True, False, False],
        [True, True, True],
        [False, False, True],
        [True, True, True],
    ],
    'T': [
        [True, True, True],
        [False, True, False],
        [False, True, False],
        [False, True, False],
        [False, True, False],
    ],
    'E': [
        [True, True, True],
        [True, False, False],
        [True, True, True],
        [True, False, False],
        [True, True, True],
    ],
    'R': [
        [True, True, True],
        [True, False, True],
        [True, True, True],
        [True, True, False],
        [True, False, True],
    ],
    'L': [
        [True, False, False],
        [True, False, False],
        [True, False, False],
        [True, False, False],
        [True, True, True],
    ],
    'I': [
        [True, True, True],
        [False, True, False],
        [False, True, False],
        [False, True, False],
        [True, True, True],
    ],
    'N': [
        [True, True, True], # Note: this 'N' differs slightly from typical 5x3, but matches your Go map
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, False, True],
    ],
    'G': [
        [False, True, True],
        [True, False, False],
        [True, False, True],
        [True, False, True],
        [False, True, False],
    ],
    'U': [
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [False, True, False],
    ],
    'C': [
        [False, True, False],
        [True, False, True],
        [True, False, False],
        [True, False, True],
        [False, True, False],
    ],
    'A': [
        [False, True, False],
        [True, False, True],
        [True, True, True],
        [True, False, True],
        [True, False, True],
    ],
    'M': [
        [True,True,True],
        [True,True,True],
        [True,False,True],
        [True,False,True],
        [True,False,True],
    ],
    'H': [
        [True,False,True],
        [True,False,True],
        [True,True,True],
        [True,False,True],
        [True,False,True],
    ],
    'O': [
        [True,True,True],
        [True,False,True],
        [True,False,True],
        [True,False,True],
        [True,True,True],
    ],
    'D': [
        [True,True,False],
        [True,False,True],
        [True,False,True],
        [True,False,True],
        [True,True,False],
    ],
    'X': [
        [True,False,True],
        [True,False,True],
        [False,True,False],
        [True,False,True],
        [True,False,True],
    ],
    'Z': [
        [True,True,True],
        [False,False,True],
        [False,True,False],
        [True,False,False],
        [True,True,True],
    ],
    'P': [
        [True,True,True],
        [True,False,True],
        [True,True,True],
        [True,False,False],
        [True,False,False],
    ],
    'K': [
        [True,False,True],
        [True,False,True],
        [True,True,False],
        [True,False,True],
        [True,False,True],
    ],
    'B': [
        [True,True,False],
        [True,False,True],
        [True,True,False],
        [True,False,True],
        [True,True,False],
    ],
    'V': [
        [True,False,True],
        [True,False,True],
        [True,False,True],
        [False,True,False],
        [False,True,False],
    ],
    'F': [
        [True,True,True],
        [True,False,False],
        [True,True,True],
        [True,False,False],
        [True,False,False],
    ],
    'W': [
        [True,False,True],
        [True,False,True],
        [True,False,True],
        [True,True,True],
        [True,False,True],
    ],
    'J': [
        [False,True,True],
        [False,False,True],
        [False,False,True],
        [True,False,True],
        [False,True,False],
    ],
    'Y': [
        [True,False,True],
        [True,False,True],
        [False,True,False],
        [False,True,False],
        [False,True,False],
    ],
    'Q': [
        [False,True,False],
        [True,False,True],
        [True,False,True],
        [True,True,True],
        [False,False,True],
    ],
    'Z': [
        [True,True,True],
        [False,False,True],
        [False,True,False],
        [True,False,False],
        [True,True,True],
    ],
    'D': [
        [True,True,False],
        [True,False,True],
        [True,False,True],
        [True,False,True],
        [True,True,False],
    ],
    'K': [
        [True,False,True],
        [True,True,False],
        [True,False,False],
        [True,True,False],
        [True,False,True],
    ],
    'X': [
        [True,False,True],
        [False,True,False],
        [False,True,False],
        [False,True,False],
        [True,False,True],
    ],
    'J': [
        [False,True,True],
        [False,False,True],
        [False,False,True],
        [True,False,True],
        [False,True,False],
    ],
    'Y': [
        [True,False,True],
        [False,True,False],
        [False,True,False],
        [False,True,False],
        [False,True,False],
    ],
    'Q': [
        [False,True,False],
        [True,False,True],
        [True,False,True],
        [True,True,True],
        [False,False,True],
    ],
    'P': [
        [True,True,True],
        [True,False,True],
        [True,True,True],
        [True,False,False],
        [True,False,False],
    ],
    'B': [
        [True,True,False],
        [True,False,True],
        [True,True,False],
        [True,False,True],
        [True,True,False],
    ],
    'V': [
        [True,False,True],
        [True,False,True],
        [True,False,True],
        [False,True,False],
        [False,True,False],
    ],
    'F': [
        [True,True,True],
        [True,False,False],
        [True,True,True],
        [True,False,False],
        [True,False,False],
    ],
    'W': [
        [True,False,True],
        [True,False,True],
        [True,False,True],
        [False,True,False],
        [False,True,False],
    ],
    'Z': [
        [True, True, True],
        [False, False, True],
        [False, True, False],
        [True, False, False],
        [True, True, True],
    ],
    'D': [
        [True, True, False],
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, True, False],
    ],
    'K': [
        [True, False, True],
        [True, True, False],
        [True, False, False],
        [True, True, False],
        [True, False, True],
    ],
    'X': [
        [True, False, True],
        [False, True, False],
        [False, True, False],
        [False, True, False],
        [True, False, True],
    ],
    'J': [
        [False, True, True],
        [False, False, True],
        [False, False, True],
        [True, False, True],
        [False, True, False],
    ],
    'Y': [
        [True, False, True],
        [False, True, False],
        [False, True, False],
        [False, True, False],
        [False, True, False],
    ],
    'Q': [
        [False, True, False],
        [True, False, True],
        [True, False, True],
        [True, True, True],
        [False, False, True],
    ],
    'P': [
        [True, True, True],
        [True, False, True],
        [True, True, True],
        [True, False, False],
        [True, False, False],
    ],
    'B': [
        [True, True, False],
        [True, False, True],
        [True, True, False],
        [True, False, True],
        [True, True, False],
    ],
    'V': [
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [False, True, False],
        [False, True, False],
    ],
    'F': [
        [True, True, True],
        [True, False, False],
        [True, True, True],
        [True, False, False],
        [True, False, False],
    ],
    'W': [
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [False, True, False],
        [False, True, False],
    ],
    'H': [
        [True, False, True],
        [True, False, True],
        [True, True, True],
        [True, False, True],
        [True, False, True],
    ],
    'O': [
        [True, True, True],
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, True, True],
    ],
    'X': [
        [True, False, True],
        [False, True, False],
        [False, True, False],
        [False, True, False],
        [True, False, True],
    ],
    'J': [
        [False, True, True],
        [False, False, True],
        [False, False, True],
        [True, False, True],
        [False, True, False],
    ],
    'Y': [
        [True, False, True],
        [False, True, False],
        [False, True, False],
        [False, True, False],
        [False, True, False],
    ],
    'Q': [
        [False, True, False],
        [True, False, True],
        [True, False, True],
        [True, True, True],
        [False, False, True],
    ],
    'P': [
        [True, True, True],
        [True, False, True],
        [True, True, True],
        [True, False, False],
        [True, False, False],
    ],
    'B': [
        [True, True, False],
        [True, False, True],
        [True, True, False],
        [True, False, True],
        [True, True, False],
    ],
    'V': [
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [False, True, False],
        [False, True, False],
    ],
    'F': [
        [True, True, True],
        [True, False, False],
        [True, True, True],
        [True, False, False],
        [True, False, False],
    ],
    'W': [
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, True, True],
        [True, False, True],
    ],
    'M': [
        [True, True, True],
        [True, True, True],
        [True, False, True],
        [True, False, True],
        [True, False, True],
    ],
    'H': [
        [True, False, True],
        [True, False, True],
        [True, True, True],
        [True, False, True],
        [True, False, True],
    ],
    'O': [
        [True, True, True],
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, True, True],
    ],
    'D': [
        [True, True, False],
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, True, False],
    ],
    'K': [
        [True, False, True],
        [True, True, False],
        [True, False, False],
        [True, True, False],
        [True, False, True],
    ],
    'X': [
        [True, False, True],
        [False, True, False],
        [False, True, False],
        [False, True, False],
        [True, False, True],
    ],
    'J': [
        [False, True, True],
        [False, False, True],
        [False, False, True],
        [True, False, True],
        [False, True, False],
    ],
    'Y': [
        [True, False, True],
        [False, True, False],
        [False, True, False],
        [False, True, False],
        [False, True, False],
    ],
    'Q': [
        [False, True, False],
        [True, False, True],
        [True, False, True],
        [True, True, True],
        [False, False, True],
    ],
    'P': [
        [True, True, True],
        [True, False, True],
        [True, True, True],
        [True, False, False],
        [True, False, False],
    ],
    'B': [
        [True, True, False],
        [True, False, True],
        [True, True, False],
        [True, False, True],
        [True, True, False],
    ],
    'V': [
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [False, True, False],
        [False, True, False],
    ],
    'F': [
        [True, True, True],
        [True, False, False],
        [True, True, True],
        [True, False, False],
        [True, False, False],
    ],
    'W': [
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, True, True],
        [True, False, True],
    ],
    # Add more letters as needed from your Go map
    ' ': [ # The space character
        [False, False, False],
        [False, False, False],
        [False, False, False],
        [False, False, False],
        [False, False, False],
    ],
}


class GameOfLifeGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = self._new_empty_grid() # Initialize with empty grid

        # Initialize random seed
        random.seed(time.time())

        self.starts = []
        self._setup_starts() # Call a method to define your patterns

        # Start with a random game, as per your Go's NewGameOfLifeGrid default
        self.NewGameRand()

    def _new_empty_grid(self):
        """Creates a new empty grid of Cell objects."""
        new_cells = [[Cell(j, i) for j in range(self.width)] for i in range(self.height)]
        return new_cells

    def get_cell(self, x, y):
        """Safely gets a cell at (x, y) or returns None if out of bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None

    def get_neighbors(self, x, y):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue # Don't count the cell itself

                nx, ny = x + j, y + i # Note: Go's grid might be X,Y vs Python's row,col
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append(self.cells[ny][nx]) # Access via [row][col]

        return neighbors

    def do_an_iteration(self):
            next_generation_states = {} # Dict to store next state: (x,y) -> bool

            for y in range(self.height):
                for x in range(self.width):
                    cell = self.cells[y][x]
                    alive_neighbors_count = 0
                    for neighbor in self.get_neighbors(x, y):
                        if neighbor.is_alive():
                            alive_neighbors_count += 1

                    # Apply Conway's rules
                    if cell.is_alive():
                        if alive_neighbors_count < 2 or alive_neighbors_count > 3:
                            next_generation_states[(x, y)] = False # Cell dies
                        else:
                            next_generation_states[(x, y)] = True  # Cell survives
                    else:
                        if alive_neighbors_count == 3:
                            next_generation_states[(x, y)] = True  # Cell becomes alive

            # Update the grid with the new states
            for (x, y), new_state in next_generation_states.items():
                self.cells[y][x].set_alive(new_state)


    def NewWithCenter(self):
        """Creates a specific pattern in the center of the grid."""
        center_h = self.height // 2
        center_w = self.width // 2

        self.clear_grid() # Clear current state first

        # Set the specific pattern
        if self.get_cell(center_w, center_h + 1):
            self.get_cell(center_w, center_h + 1).set_alive()
        if self.get_cell(center_w, center_h):
            self.get_cell(center_w, center_h).set_alive()
        if self.get_cell(center_w, center_h - 1):
            self.get_cell(center_w, center_h - 1).set_alive()
        if self.get_cell(center_w + 1, center_h + 1):
            self.get_cell(center_w + 1, center_h + 1).set_alive()
        if self.get_cell(center_w - 1, center_h):
            self.get_cell(center_w - 1, center_h).set_alive()

    def NewGameRand(self):
        """Initializes the grid with a random pattern."""
        self.clear_grid() # Clear current state first
        for row in self.cells:
            for cell in row:
                if random.randint(0, 1) == 1: # 50% chance
                    cell.set_alive(True)
                else:
                    cell.set_alive(False)

    def NewGameLetters(self, message: str):
        """Draws a text message onto the grid as a pattern."""
        center_row_start = (self.height // 3)
        center_col_start = (self.width // 2) - 25 # Roughly centers a long word

        self.clear_grid() # Clear current state first

        upper_message = message.upper()
        current_col = center_col_start
        current_row = center_row_start

        for char in upper_message:

            if char == ' ':
                current_col += 7 # Advance column for a space
                continue

            letter_pattern = letters.get(char)
            if not letter_pattern:
                # If char not found, default to NewWithCenter, like your Go code
                self.NewWithCenter()
                return

            for row_offset in range(5): # 5 rows for letter pattern
                for col_offset in range(3): # 3 columns for letter pattern
                    if letter_pattern[row_offset][col_offset]:
                        target_x = current_col + col_offset
                        target_y = current_row + row_offset
                        cell = self.get_cell(target_x, target_y)
                        if cell: # Check bounds before setting
                            cell.set_alive(True)
            
            current_col += 5 # Advance column for next letter

    def clear_grid(self):
        """Sets all cells in the grid to dead."""
        for row in self.cells:
            for cell in row:
                cell.set_dead()

    def _setup_starts(self):
        """Populates the list of callable starting patterns."""
        self.starts.append(self.NewWithCenter)
        self.starts.append(lambda: self.NewGameLetters("STERLING URGENT CARE"))
        self.starts.append(lambda: self.NewGameLetters("RESURGENCE"))
        self.starts.append(lambda: self.NewGameLetters("RESTARTING"))
        self.starts.append(lambda: self.NewGameLetters("REGULATING"))
        self.starts.append(lambda: self.NewGameLetters("ULCERATING"))
        self.starts.append(lambda: self.NewGameLetters("GLISTENING"))
        self.starts.append(lambda: self.NewGameLetters("RELUCTANCE"))
        self.starts.append(lambda: self.NewGameLetters("SULTRINESS"))
        self.starts.append(lambda: self.NewGameLetters("INCARNATE"))
        self.starts.append(lambda: self.NewGameLetters("INCULCATE"))
        self.starts.append(lambda: self.NewGameLetters("LITIGATES"))
        self.starts.append(lambda: self.NewGameLetters("REGULATES"))
        self.starts.append(lambda: self.NewGameLetters("RESCALING"))
        self.starts.append(lambda: self.NewGameLetters("CELL"))
        self.starts.append(lambda: self.NewGameLetters("RISE"))
        self.starts.append(lambda: self.NewGameLetters("GENES"))
        self.starts.append(lambda: self.NewGameLetters("NUCLEI"))
        self.starts.append(lambda: self.NewGameLetters("CULTURE"))
        self.starts.append(lambda: self.NewGameLetters("GLINT"))
        self.starts.append(lambda: self.NewGameLetters("TRUST"))
        self.starts.append(self.NewGameRand) # Random pattern at the end