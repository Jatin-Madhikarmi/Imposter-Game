import pygame
import sys

# --- INITIALIZATION ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Imposter Game")

# Colors & Fonts
BLACK, WHITE, GRAY = (0, 0, 0), (255, 255, 255), (200, 200, 200)
font_title = pygame.font.SysFont("Arial", 64, bold=True)
font_ui = pygame.font.SysFont("Arial", 32)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)

# --- THE INTEGRATED GAME CLASS ---
class Game:
    def __init__(self):
        self.state = "MENU"  # Current screen
        self.categories = ["Animals", "Food", "Places", "Objects"]
        self.current_cat_idx = 0
        self.player_count = 3
        self.word_database={
            "Animals":"Lion",
            "Food":"Pizza",
            "Places":"Kathmandu",
            "Objects":"Nail Cutter"
        }
        
        # Player Input Data
        self.player_names = []
        self.current_text = ""
        self.naming_idx = 1 # Tracks which player we are naming

    def handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.current_cat_idx = (self.current_cat_idx + 1) % len(self.categories)
            if event.key == pygame.K_LEFT:
                self.current_cat_idx = (self.current_cat_idx - 1) % len(self.categories)
            if event.key == pygame.K_UP and self.player_count < 10:
                self.player_count += 1
            if event.key == pygame.K_DOWN and self.player_count > 3:
                self.player_count -= 1
            if event.key == pygame.K_SPACE:
                self.state = "INPUT_NAMES"

    def handle_input_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.current_text.strip() != "":
                    self.player_names.append(self.current_text.strip())
                    self.current_text = ""
                    self.naming_idx += 1
                    if self.naming_idx > self.player_count:
                        self.state = "ROLE_ASSIGNMENT" # Next screen
            elif event.key == pygame.K_BACKSPACE:
                self.current_text = self.current_text[:-1]
            else:
                if len(self.current_text) < 15:
                    self.current_text += event.unicode

    def run(self):
        while True:
            screen.fill(BLACK)
            
            # 1. EVENT HANDLING
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if self.state == "MENU":
                    self.handle_menu_events(event)
                elif self.state == "INPUT_NAMES":
                    self.handle_input_events(event)

            # 2. RENDERING (DRAWING)
            if self.state == "MENU":
                draw_text("IMPOSTER GAME", font_title, WHITE, SCREEN_WIDTH//2, 100)
                draw_text(f"Category: {self.categories[self.current_cat_idx]}", font_ui, WHITE, SCREEN_WIDTH//2, 250)
                draw_text(f"Players: {self.player_count}", font_ui, WHITE, SCREEN_WIDTH//2, 400)
                draw_text("Press SPACE to Start", font_ui, GRAY, SCREEN_WIDTH//2, 530)

            elif self.state == "INPUT_NAMES":
                draw_text(f"Enter Name for Player {self.naming_idx}", font_ui, WHITE, SCREEN_WIDTH//2, 150)
                # Draw Input Box
                pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2 - 150, 250, 300, 50), 2)
                draw_text(self.current_text, font_ui, WHITE, SCREEN_WIDTH//2, 275)
                draw_text("Press ENTER to confirm", font_ui, GRAY, SCREEN_WIDTH//2, 400)

            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()