import pygame
import sys
import random

# Initialize Pygame here
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Galaxia")

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Load background music
pygame.mixer.music.load("game.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)# -1 means the music will loop indefinitely

# Load explosion sfx
explosion_sound = pygame.mixer.Sound("explosion.mp3")
explosion_sound.set_volume(1.0)

# Load shooting sound
shooting_sound = pygame.mixer.Sound("laser.mp3")
shooting_sound.set_volume(0.2)

# Load explosion image
explosion_image = pygame.image.load("explosion.png").convert_alpha()
explosion_image = pygame.transform.scale(explosion_image, (150, 150))  # Adjust the size as needed

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

# Load weapon supply image
weapon_supply_image = pygame.image.load("weapon_supply.png").convert_alpha()
weapon_supply_image = pygame.transform.scale(weapon_supply_image, (80, 80))

# Game objects
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.speed = 1
        self.lives = 3
        self.bullet_count = 1

    def update(self, keys):
        if keys[pygame.K_LEFT]:  # Allow continuous movement to the left
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:  # Allow continuous movement to the right
            self.rect.x += self.speed
        # Ensure the player stays within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

    def shoot(self):
        if self.bullet_count == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
        elif self.bullet_count == 2:
            bullet1 = Bullet(self.rect.left, self.rect.top)
            bullet2 = Bullet(self.rect.right, self.rect.top)
            all_sprites.add(bullet1, bullet2)
            bullets.add(bullet1, bullet2)
        elif self.bullet_count >= 3:
            bullet1 = Bullet(self.rect.left, self.rect.top)
            bullet2 = Bullet(self.rect.centerx, self.rect.top)
            bullet3 = Bullet(self.rect.right, self.rect.top)
            all_sprites.add(bullet1, bullet2, bullet3)
            bullets.add(bullet1, bullet2, bullet3)
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

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = explosion_image
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 100  # Duration of the explosion effect

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()

class WeaponSupply(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = weapon_supply_image
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), -20))
        self.speed = 0.9

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# def game_over():
#     game_over_text = font.render("Game Over", True, WHITE)
#     game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#     screen.blit(game_over_text, game_over_rect)
#     pygame.display.flip()
#     pygame.time.wait(2000)
#     main_menu()

def game_over(score):
    running = True
    while running:
        screen.fill((0, 0, 0))

        for star in stars:
            star.move()
            star.draw(screen)

        settings_text = font.render("GAME OVER", True, WHITE)
        settings_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(settings_text, settings_rect)

        score_text = font.render("Your Score is " + str(score), True, YELLOW)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 70))
        screen.blit(score_text, score_rect)

        vertical_gap = 80
        resume_btn = create_button("Replay", WIDTH // 2, HEIGHT // 2)
        settings_btn = create_button("Settings", WIDTH // 2, HEIGHT // 2 + vertical_gap)
        exit_btn = create_button("Exit", WIDTH // 2, HEIGHT // 2 + 2 * vertical_gap)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if resume_btn.collidepoint(mouse_pos):
                    main_game()
                elif settings_btn.collidepoint(mouse_pos):
                    print("Settings button clicked")
                elif exit_btn.collidepoint(mouse_pos):
                    main_menu()

        pygame.display.flip()

def pause_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))

        for star in stars:
            star.move()
            star.draw(screen)

        settings_text = font.render("PAUSE", True, WHITE)
        settings_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(settings_text, settings_rect)

        vertical_gap = 80
        resume_btn = create_button("Resume", WIDTH // 2, HEIGHT // 2)
        settings_btn = create_button("Settings", WIDTH // 2, HEIGHT // 2 + vertical_gap)
        exit_btn = create_button("Exit", WIDTH // 2, HEIGHT // 2 + 2 * vertical_gap)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if resume_btn.collidepoint(mouse_pos):
                    running = False
                elif settings_btn.collidepoint(mouse_pos):
                    print("Settings button clicked")
                elif exit_btn.collidepoint(mouse_pos):
                    main_menu()

        pygame.display.flip()

def main_game():
    global all_sprites, bullets, enemies, explosions, weapon_supplies
    # Re-initialize sprite groups
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    weapon_supplies = pygame.sprite.Group()
    
    player = Player()
    all_sprites.add(player)

    LEVELS = 3  # Total number of levels
    level = 1   # Current level
    level_score_requirement = 10  
    score = 0
    lives = player.lives

    enemy_spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn_event, 1000)

    weapon_supply_event = pygame.USEREVENT + 2
    pygame.time.set_timer(weapon_supply_event, 5000)  # Adjust the time as needed

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                elif event.key == pygame.K_ESCAPE:
                    pause_menu()
            elif event.type == enemy_spawn_event:
                enemy = Enemy(random.randint(0, WIDTH - 40), -40)
                all_sprites.add(enemy)
                enemies.add(enemy)
            elif event.type == weapon_supply_event:
                weapon_supply = WeaponSupply()
                all_sprites.add(weapon_supply)
                weapon_supplies.add(weapon_supply)

        keys = pygame.key.get_pressed()
        player.update(keys)

        for sprite in all_sprites:
            if sprite != player:
                sprite.update()

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 1
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            explosions.add(explosion)
            explosion_sound.play()

        enemy_hits = pygame.sprite.spritecollide(player, enemies, True)
        if enemy_hits:
            player.lives -= 1
            lives -= 1
            if player.lives <= 0:
                game_over(score)

        supply_hits = pygame.sprite.spritecollide(player, weapon_supplies, True)
        for supply in supply_hits:
            player.bullet_count += 1

        # Check if the player has reached the score requirement for the next level
        if score >= level * level_score_requirement and level < LEVELS:
            level += 1
            # Adjust any level-specific parameters here, like enemy spawn rate
            pygame.time.set_timer(enemy_spawn_event, 1000 // level)

        # Drawing
        screen.fill((0, 0, 0))
        for star in stars:
            star.move()
            star.draw(screen)
        
        all_sprites.draw(screen)

        score_text = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        lives_text = score_font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (WIDTH - 110, 10))

        # Display current level
        level_text = score_font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (WIDTH // 2 - 50, 10))

        pygame.display.flip()

def main_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))

        for star in stars:
            star.move()
            star.draw(screen)

        title_text = font.render("Galaxia", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        vertical_gap = 80

        single_player_btn = create_button("Single Player", WIDTH // 2, HEIGHT // 2)
        multiplayer_btn = create_button("Multiplayer", WIDTH // 2, HEIGHT // 2 + vertical_gap)
        scores_btn = create_button("Scores", WIDTH // 2, HEIGHT // 2 + 2 * vertical_gap)
        settings_btn = create_button("Settings", WIDTH // 2, HEIGHT // 2 + 3 * vertical_gap)
        exit_btn = create_button("Exit", WIDTH // 2, HEIGHT // 2 + 4 * vertical_gap)

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
                elif exit_btn.collidepoint(mouse_pos):
                    running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Start the main menu
main_menu()
