import pygame
import sys
import random

# --- INITIALIZATION ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Imposter Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY  = (100, 100, 100)
RED   = (255, 0, 0)

# Fonts
font_title = pygame.font.SysFont("Arial", 64, bold=True)
font_ui = pygame.font.SysFont("Arial", 32)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)



def get_random_word(category):
    words = {
        "Animals": ["Lion", "Tiger", "Elephant", "Mouse", "Peacock", "Sparrow"],
        "Food": ["Pizza", "Momo", "Bhat Dhal", "Fried Rice", "Chowmein", "Veg Khana Set"],
        "Places": ["Chitlang", "Dhulikhel", "Banepa", "Lalitpur", "Bhaktapur", "Kathmandu"],
        "Objects": ["Pencil", "Pen", "Duster", "Board", "Nails", "Hammer"]
    }
    # Return a single random word from the chosen category
    return random.choice(words[category])
class Game:
    def __init__(self):
        self.state = "MENU"
        self.categories = ["Animals", "Food", "Places", "Objects"]
        self.word_database = {}
        
        # State Variables
        self.current_cat_idx = 0
        self.player_count = 3
        self.player_names = []
        self.current_text = ""
        self.naming_idx = 1
        
        # Role Assignment Variables
        self.roles = []
        self.secret_word = ""
        self.current_player_viewing = 0
        self.showing_back = True  # True = Name side, False = Role side
        self.anim_width = 200
        self.is_flipping = False
        self.flip_speed = 15

        #Voting Variables
        self.votes={}
        self.voted_count=0

    def setup_roles(self):
        """Logic to assign imposters and words"""
        selected_category = self.categories[self.current_cat_idx]
        self.secret_word = get_random_word(selected_category)
        num_imposters = 2 if self.player_count > 5 else 1
        
        self.roles = ["Civilian"] * (self.player_count - num_imposters)
        for _ in range(num_imposters):
            self.roles.append("Imposter")
        random.shuffle(self.roles)

        self.current_player_viewing=0
        self.showing_back=True

    def update_animation(self):
        """The math for the 2D scaling (pseudo-rotation)"""
        if self.is_flipping:
            self.anim_width -= self.flip_speed
            if self.anim_width <= 0:
                self.anim_width = 0
                self.showing_back = not self.showing_back
                self.flip_speed *= -1 
            if self.anim_width > 200:
                self.anim_width = 200
                self.is_flipping = False
                self.flip_speed = abs(self.flip_speed)

    def setup_voting(self):
        self.votes={name : 0 for name in self.player_names}
        self.voted_count=0

    def draw_voting_screen(self):
        draw_text("VOTING PHASE",font_title,WHITE,SCREEN_WIDTH//2,50)
        draw_text(f"Votes Cast:{self.voted_count}/{self.player_count}",font_ui,GRAY,SCREEN_WIDTH//2,100)

        mouse_pos=pygame.mouse.get_pos()

        start_y=180
        for i,name in enumerate(self.player_names):
            rect=pygame.Rect(SCREEN_WIDTH//2-150,start_y+(i*60),300,50)

            color =RED if rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(screen,color,rect,2,border_radius=10)

            vote_text=f"{name}:{self.votes[name]} votes"
            draw_text(vote_text,font_ui,color,SCREEN_WIDTH//2,rect.centery)

    def handle_voting_events(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos=pygame.mouse.get_pos()
            start_y=180
            for i, name in enumerate(self.player_names):
                rect=pygame.Rect(SCREEN_WIDTH//2-150,start_y+(i*60),300,50)
                if rect.collidepoint(mouse_pos):
                    self.votes[name]+=1
                    self.voted_count+=1

                    if self.voted_count >= self.player_count:
                        self.state="GAME_OVER"

    def get_results(self):
        winner_name=max(self.votes,key=self.votes.get)
        max_votes=self.votes[winner_name]

        vote_counts=list(self.votes.values())
        if vote_counts.count(max_votes) > 1:
            return "YOU LOST"
        
        winner_idx=self.player_names.index(winner_name)
        if self.roles[winner_idx] == "Imposter":
            return "YOU WON"
        
        else:
            return "YOU LOST"
        
    def draw_game_over(self):
        result_text=self.get_results()

        color=(0,255,0) if result_text=="YOU WON" else RED

        draw_text(result_text,font_title,color,SCREEN_WIDTH//2,150)

        imposter_name=[self.player_names[i] for i,role in enumerate(self.roles) if role== "Imposter"]
        draw_text(f"The imposter was: {','.join(imposter_name)}",font_ui,WHITE,SCREEN_WIDTH//2,250)

        mouse_pos=pygame.mouse.get_pos()
        play_rect=pygame.Rect(SCREEN_WIDTH//2-150,350,300,50)
        quit_rect=pygame.Rect(SCREEN_WIDTH//2-150,430,300,50)


        p_color=GRAY if play_rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen,p_color,play_rect,2,border_radius=10)
        draw_text("PLAY AGAIN",font_ui,p_color,SCREEN_WIDTH//2,375)

        q_color=GRAY if quit_rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen,q_color,quit_rect,2,border_radius=10)
        draw_text("QUIT",font_ui,q_color,SCREEN_WIDTH//2,455)

        return play_rect,quit_rect
    
    def handle_game_over_events(self,event,play_rect,quit_rect):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                self.__init__()
                self.state="MENU"

            elif quit_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            screen.fill(BLACK)
            
            # --- 1. EVENT HANDLING ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if self.state == "MENU":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT: self.current_cat_idx = (self.current_cat_idx + 1) % len(self.categories)
                        if event.key == pygame.K_UP and self.player_count < 10: self.player_count += 1
                        if event.key == pygame.K_DOWN and self.player_count > 3: self.player_count -= 1
                        if event.key == pygame.K_SPACE: self.state = "INPUT_NAMES"

                elif self.state == "INPUT_NAMES":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and self.current_text.strip():
                            self.player_names.append(self.current_text.strip())
                            self.current_text = ""
                            self.naming_idx += 1
                            if self.naming_idx > self.player_count:
                                self.setup_roles()
                                self.state = "ROLE_ASSIGNMENT"
                        elif event.key == pygame.K_BACKSPACE: self.current_text = self.current_text[:-1]
                        else: self.current_text += event.unicode

                elif self.state == "ROLE_ASSIGNMENT":
                    if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                        if not self.is_flipping:
                            # If we just saw the role, move to next player on next click
                            if not self.showing_back:
                                self.current_player_viewing += 1
                                if self.current_player_viewing >= self.player_count:
                                    self.setup_voting()
                                    self.state = "VOTING_SCREEN" # Final transition
                                else:
                                    self.is_flipping = True # Flip back to name side for next player
                            else:
                                self.is_flipping = True
                
                elif self.state == "VOTING_SCREEN":
                    self.handle_voting_events(event)
                    
                elif self.state=="GAME_OVER":
                    play_btn,quit_btn=self.draw_game_over()
                    self.handle_game_over_events(event,play_btn,quit_btn)
            
                    

            # --- 2. UPDATE LOGIC ---
            if self.state == "ROLE_ASSIGNMENT":
                self.update_animation()

            # --- 3. RENDERING ---
            if self.state == "MENU":
                draw_text("IMPOSTER GAME", font_title, WHITE, SCREEN_WIDTH//2, 100)
                draw_text(f"Category: {self.categories[self.current_cat_idx]}", font_ui, WHITE, SCREEN_WIDTH//2, 250)
                draw_text("Forward arrows for changing the category",font_ui,WHITE,SCREEN_WIDTH//2,300)
                draw_text(f"Players: {self.player_count}", font_ui, WHITE, SCREEN_WIDTH//2, 400)
                draw_text("Up and Down arrows for changing the category",font_ui,WHITE,SCREEN_WIDTH//2,450)
                draw_text("Press SPACE to Start", font_ui, GRAY, SCREEN_WIDTH//2, 530)

            elif self.state == "INPUT_NAMES":
                draw_text(f"Name for Player {self.naming_idx}", font_ui, WHITE, SCREEN_WIDTH//2, 150)
                pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2 - 150, 250, 300, 50), 2)
                draw_text(self.current_text, font_ui, WHITE, SCREEN_WIDTH//2, 275)

            elif self.state == "ROLE_ASSIGNMENT":
                draw_text("Click Card to Flip", font_ui, GRAY, SCREEN_WIDTH//2, 100)
                
                # The Card Shape (Animated width)
                card_rect = pygame.Rect(0, 0, self.anim_width, 300)
                card_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                pygame.draw.rect(screen, WHITE, card_rect, border_radius=15)
                
                # Show Content only if card is wide enough
                if self.anim_width > 50:
                    if self.showing_back:
                        name = self.player_names[self.current_player_viewing]
                        draw_text(name, font_ui, BLACK, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                    else:
                        role = self.roles[self.current_player_viewing]
                        if role == "Imposter":
                            draw_text("IMPOSTER", font_ui, RED, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                        else:
                            draw_text(self.secret_word, font_ui, BLACK, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

            elif self.state=="VOTING_SCREEN":
                self.draw_voting_screen()

            elif self.state == "GAME_OVER":
                self.draw_game_over()
                

            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()