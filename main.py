import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
ACCENT = (50, 150, 255)

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Imposter Game")
font_title = pygame.font.SysFont("Arial", 64, bold=True)
font_ui = pygame.font.SysFont("Arial", 32)

# Game Data for Selection
categories = ["Animals", "Food", "Places", "Objects"]
current_cat_idx = 0
player_count = 3

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)

def main_menu():
    global current_cat_idx, player_count
    
    while True:
        screen.fill(BLACK)
        
        # 1. Title
        draw_text("IMPOSTER GAME", font_title, WHITE, SCREEN_WIDTH//2, 100)
        
        # 2. Category Selection Field
        draw_text(f"Category: {categories[current_cat_idx]}", font_ui, WHITE, SCREEN_WIDTH//2, 250)
        draw_text("< Press Left/Right to Change >", font_ui, GRAY, SCREEN_WIDTH//2, 290)
        
        # 3. Player Selection Field
        draw_text(f"Players: {player_count}", font_ui, WHITE, SCREEN_WIDTH//2, 400)
        draw_text("< Press Up/Down to Change (3-10) >", font_ui, GRAY, SCREEN_WIDTH//2, 440)

        # 4. Start Prompt
        draw_text("Press SPACE to Start", font_ui, ACCENT, SCREEN_WIDTH//2, 530)

        for event in pygame.event.get():
            print(type(pygame.event.get()))
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # Category Logic
                if event.key == pygame.K_RIGHT:
                    current_cat_idx = (current_cat_idx + 1) % len(categories)
                if event.key == pygame.K_LEFT:
                    current_cat_idx = (current_cat_idx - 1) % len(categories)
                
                # Player Count Logic
                if event.key == pygame.K_UP and player_count < 10:
                    player_count += 1
                if event.key == pygame.K_DOWN and player_count > 3:
                    player_count -= 1
                
                # Start Game
                if event.key == pygame.K_SPACE:
                    print(f"Starting Game: {categories[current_cat_idx]} with {player_count} players")
                    return # This would move to the next screen

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()