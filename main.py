import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)

# Load background music
pygame.mixer.music.load("game.mp3")
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Load shooting sound
shooting_sound = pygame.mixer.Sound("laser.mp3")

# Font
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 36)

# Star class for the animated background
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(1, 3)

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -self.size
            self.x = random.randint(0, WIDTH)

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)

# Create a list of stars
stars = [Star() for _ in range(100)]

# Button function
def create_button(text, center_x, center_y):
    text_render = button_font.render(text, True, WHITE)
    rect = text_render.get_rect(center=(center_x, center_y))
    pygame.draw.rect(screen, GRAY, rect.inflate(20, 20))
    screen.blit(text_render, rect)
    return rect

player_image = pygame.image.load("player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.image.load("enemy.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (100, 100))
# Game objects
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.speed = 1 # Adjust the player's movement speed
        self.lives = 3

    def update(self, keys):
        if keys[pygame.K_LEFT]:  # Allow continuous movement to the left
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:  # Allow continuous movement to the right
            self.rect.x += self.speed
        # Ensure the player stays within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

        # Adjust the speed of the player's movement

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shooting_sound.play()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 0.6  # Adjust the speed of the enemies

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:  # Check if the enemy is off the screen
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(RED)  # Set the bullet color to red
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


def game_over():
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    main_menu()

def main_game():
    player = Player()
    all_sprites.add(player)

    score = 0
    lives = player.lives

    enemy_spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn_event, 1000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            elif event.type == enemy_spawn_event:
                enemy = Enemy(random.randint(0, WIDTH - 40), -40)
                all_sprites.add(enemy)
                enemies.add(enemy)

        keys = pygame.key.get_pressed()

        player.update(keys)  # Update the player with keys

        for sprite in all_sprites:
            if sprite != player:
                sprite.update()  # Update other sprites without arguments

        # Check for collisions
        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 10

        enemy_hits = pygame.sprite.spritecollide(player, enemies, True)
        if enemy_hits:
            player.lives -= 1
            lives -= 1
            if player.lives <= 0:
                game_over()

        # Drawing
        screen.fill((0, 0, 0))
        for star in stars:
            star.move()
            # star.draw(screen)
        
        # enemies.draw(screen)

        all_sprites.draw(screen)

        score_text = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        lives_text = score_font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (WIDTH - 110, 10))

        pygame.display.flip()


def main_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))

        for star in stars:
            star.move()
            star.draw(screen)

        # Title
        title_text = font.render("Space Shooter", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Buttons
        single_player_btn = create_button("Single Player", WIDTH // 2, HEIGHT // 2 - 60)
        multiplayer_btn = create_button("Multiplayer", WIDTH // 2, HEIGHT // 2)
        scores_btn = create_button("Scores", WIDTH // 2, HEIGHT // 2 + 60)
        settings_btn = create_button("Settings", WIDTH // 2, HEIGHT // 2 + 120)

    

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if single_player_btn.collidepoint(mouse_pos):
                    main_game()
                elif multiplayer_btn.collidepoint(mouse_pos):
                    print("Multiplayer button clicked")
                elif scores_btn.collidepoint(mouse_pos):
                    print("Scores button clicked")
                elif settings_btn.collidepoint(mouse_pos):
                    print("Settings button clicked")

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Start the main menu
main_menu()
