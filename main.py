import pygame
from game import Game

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Fonts
font = pygame.font.SysFont(None, 75)

def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(white)
        title_text = font.render("Space Shooter", True, black)
        play_text = font.render("Play", True, black)
        screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, screen_height//2 - 100))
        play_button = screen.blit(play_text, (screen_width//2 - play_text.get_width()//2, screen_height//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    menu_running = False
                    game_loop()

        pygame.display.update()

def game_loop():
    game = Game(screen, screen_width, screen_height)
    game.run()

if __name__ == "__main__":
    main_menu()
    pygame.quit()
