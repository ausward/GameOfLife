import pygame
import sys
import time

# Assuming your Game of Life logic is in a file named 'life.py'
from life import GameOfLifeGrid

# --- Constants ---
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
CELL_SIZE = 10 # Matches your Go code's cellSize

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        pygame.init() # Initialize all the Pygame modules

        icon = pygame.image.load("icon.png") # Load an icon image
        pygame.display.set_icon(icon) # Set the window icon

        # Get actual monitor resolution (optional, but good for fullscreen)
        infoObject = pygame.display.Info()
        self.screen_width = infoObject.current_w
        self.screen_height = infoObject.current_h

        # Setup the display surface
        # Use FULLSCREEN flag for a direct fullscreen experience
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Go Way Of Life (Python/Pygame)")
        pygame.mouse.set_visible(False) # Often desired for kiosk apps

        # Game of Life grid dimensions
        grid_width = self.screen_width // CELL_SIZE
        grid_height = self.screen_height // CELL_SIZE
        self.life_grid = GameOfLifeGrid(grid_width, grid_height)

        self.tps = 100 # Ticks Per Second (simulation speed)
        self.last_update_time = time.time() # For managing simulation speed
        self.last_pattern_change_time = time.time() # For managing pattern changes

        self.r, self.g, self.b = 255, 255, 255 # RGB color for alive cells
        self.start_index = 0

        self.clock = pygame.time.Clock() # For managing frame rate

    def run(self):
        running = True
        while running:
            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # Allow ESC to quit
                        running = False
                    if event.key == pygame.K_n:
                        self.last_pattern_change_time = time.time() - (20 * 60 * 60) # Simulate 20 hours passed
                    if event.key == pygame.K_s and self.tps > 1:
                        self.tps -= 1
                    if event.key == pygame.K_f:
                        self.tps += 1
                    # if event.key == pygame.K_m: # Example for NewGameLetters
                    #     self.life_grid.new_game_letters("STERLING URGENT CARE")

            # --- Game Logic Update (based on TPS) ---
            current_time = time.time()
            # if current_time - self.last_update_time >= 1.0 / self.tps:
            self.life_grid.do_an_iteration()
            self.last_update_time = current_time

            # Color change logic (from your Go code)
            self.b = (self.b - 2) % 256 # Ensure it wraps around 0-255
            self.g = (self.g + 3) % 256 # Ensure it wraps around 0-255

            # --- Pattern Change Logic (from your Go code) ---
            if current_time - self.last_pattern_change_time >= 2 * 60: # 10 minutes
                self.last_pattern_change_time = current_time
                temp_index = self.start_index
                if temp_index >= len(self.life_grid.starts): # Check bounds
                    temp_index = 0
                    self.start_index = 0
                else:
                    self.start_index += 1
                
                # Execute the pattern function
                if self.life_grid.starts: # Ensure there are patterns defined
                    self.life_grid.starts[temp_index]()


            # --- Drawing ---
            self.screen.fill(BLACK) # Clear the screen each frame

            for row in self.life_grid.cells:
                for cell in row:
                    if cell.is_alive():
                        cell_rect = pygame.Rect(
                            cell.x * CELL_SIZE,
                            cell.y * CELL_SIZE,
                            CELL_SIZE,
                            CELL_SIZE
                        )
                        pygame.draw.rect(self.screen, (self.r, self.g, self.b), cell_rect)

            pygame.display.flip() # Update the full display Surface to the screen

            self.clock.tick(120) # Limit frame rate to 60 FPS

        pygame.quit() # Uninitialize Pygame modules
        sys.exit() # Exit the program

if __name__ == "__main__":
    game = Game()
    game.run()
