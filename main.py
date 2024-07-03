import pygame
import sys
import random
import math

# Initialize Pygame her
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
pygame.mixer.music.load("./assets/game.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)  # -1 means the music will loop indefinitely

# Load explosion sfx
explosion_sound = pygame.mixer.Sound("./assets/explosion.mp3")
explosion_sound.set_volume(1.0)

# Load shooting sound
shooting_sound = pygame.mixer.Sound("./assets/laser.mp3")
shooting_sound.set_volume(0.2)

# Load explosion image
explosion_image = pygame.image.load("./assets/explosion.png").convert_alpha()
explosion_image = pygame.transform.scale(explosion_image, (150, 150))  # Adjust the size as needed

# Load images for player and enemies
# player_image = pygame.image.load("./assets/player.png").convert_alpha()
# player_image = pygame.transform.scale(player_image, (50, 50))
character_images = []
for i in range(1, 6):
    image = pygame.image.load(f"./assets/character_{i}.png").convert_alpha()
    image = pygame.transform.scale(image, (50, 50))  # Adjust size as needed
    character_images.append(image)

# Set the default player image
current_character_index = 0
player_image = character_images[current_character_index]
enemy_image = pygame.image.load("./assets/enemy.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (100, 100))
alien_ship_image = pygame.image.load("./assets/alien_ships.png").convert_alpha()
alien_ship_image = pygame.transform.scale(alien_ship_image, (100, 100))

# Font
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 36)

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Game constants
ENEMY_COUNT = 20
enemy_spawned = False

# Star class for the animated background
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 1)
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


# player_image = pygame.image.load("./assets/player.png").convert_alpha()
# player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.image.load("./assets/enemy.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (100, 100))

# Load weapon supply image
weapon_supply_image = pygame.image.load("./assets/weapon_supply.png").convert_alpha()
weapon_supply_image = pygame.transform.scale(weapon_supply_image, (80, 80))

def draw_volume_bar(label, volume, pos_x, pos_y):
    bar_width = 200
    bar_height = 20
    fill_width = int(volume * bar_width)
    text_margin = 10  # Margin between the text and the bar
    
    # Draw label
    label_text = score_font.render(label, True, WHITE)
    label_rect = label_text.get_rect(midright=(pos_x - text_margin, pos_y))
    screen.blit(label_text, label_rect)
    
    # Draw bar background
    pygame.draw.rect(screen, GRAY, (pos_x, pos_y - bar_height//2, bar_width, bar_height))
    # Draw filled part of the bar
    pygame.draw.rect(screen, YELLOW, (pos_x, pos_y - bar_height//2, fill_width, bar_height))
    # Draw bar border
    pygame.draw.rect(screen, WHITE, (pos_x, pos_y - bar_height//2, bar_width, bar_height), 2)

    return pygame.Rect(pos_x, pos_y - bar_height//2, bar_width, bar_height)


def settings_menu():
    global player_image, current_character_index

    running = True
    music_volume = pygame.mixer.music.get_volume()
    sfx_volume = explosion_sound.get_volume()

    while running:
        screen.fill((0, 0, 0))

        for star in stars:
            star.move()
            star.draw(screen)

        settings_text = font.render("Settings", True, WHITE)
        settings_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(settings_text, settings_rect)

        music_bar = draw_volume_bar("Music Volume", music_volume, WIDTH // 2 + 100, HEIGHT // 2 - 60)
        sfx_bar = draw_volume_bar("SFX Volume", sfx_volume, WIDTH // 2 + 100, HEIGHT // 2 + 20)

        back_btn = create_button("Back", WIDTH // 2, HEIGHT // 2 + 300)

        # Display "Choose Character" title
        character_text = score_font.render("Choose Character:", True, WHITE)
        character_rect = character_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(character_text, character_rect)

        # Display character options
        character_y = HEIGHT // 2 + 120  # Position below the title
        character_x_start = WIDTH // 2 - (len(character_images) * 50 + (len(character_images) - 1) * 10) // 2
        character_margin = 10

        character_rects = []
        for i, image in enumerate(character_images):
            character_x = character_x_start + i * (image.get_width() + character_margin)
            rect = screen.blit(image, (character_x, character_y))
            character_rects.append(rect)
            if i == current_character_index:
                pygame.draw.rect(screen, YELLOW, rect, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_btn.collidepoint(mouse_pos):
                    running = False
                elif music_bar.collidepoint(mouse_pos):
                    music_volume = (mouse_pos[0] - music_bar.x) / music_bar.width
                    pygame.mixer.music.set_volume(music_volume)
                elif sfx_bar.collidepoint(mouse_pos):
                    sfx_volume = (mouse_pos[0] - sfx_bar.x) / sfx_bar.width
                    explosion_sound.set_volume(sfx_volume)
                    shooting_sound.set_volume(sfx_volume)
                else:
                    for i, rect in enumerate(character_rects):
                        if rect.collidepoint(mouse_pos):
                            current_character_index = i
                            player_image = character_images[current_character_index]
                            break

        pygame.display.flip()



# Game objects
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.speed = 1  # Adjust this value to change the player's ship speed
        self.lives = 3
        self.bullet_count = 1

    def update(self, keys):
        # Move the player's ship based on the keys pressed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
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

    def set_image(self, image):
        self.image = image
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect(topleft=(x, 0))  # Start at the top of the screen
        self.target_y = y  # The designated position
        self.speed_y = random.uniform(0.5, 1.0)
        self.speed_x = random.uniform(0.8, 1.5)
        self.amplitude = random.uniform(30, 80)
        self.frequency = random.uniform(0.01, 0.03)
        self.start_x = x
        self.time = 0
        self.oscillate = random.choice([True, False])
        self.horizontal = random.choice([True, False])
        self.oscillate_start_y = random.randint(HEIGHT // 4, HEIGHT // 2)
        self.dropping = True  # Initial state is dropping down

    def update(self):
        if self.dropping:
            self.rect.y += self.speed_y
            if self.rect.y >= self.target_y:
                self.rect.y = self.target_y
                self.dropping = False  # Stop dropping and start normal behavior
        else:
            if self.horizontal:
                self.rect.x += self.speed_x
                if self.rect.left <= 0 or self.rect.right >= WIDTH:
                    self.speed_x *= -1
            else:
                if self.rect.y < self.oscillate_start_y:
                    self.rect.y += self.speed_y
                else:
                    if self.oscillate:
                        new_x = self.start_x + self.amplitude * math.sin(self.frequency * self.time)
                        if abs(new_x - self.rect.x) > 1:  # Ensure noticeable movement
                            self.rect.x = new_x
                    self.time += 1

            # Ensure the enemy stays within the screen boundaries
            self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))


class AlienShip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = alien_ship_image
        self.rect = self.image.get_rect(topleft=(x, 0))  # Start at the top of the screen
        self.target_y = y  # The designated position
        self.speed_y = random.uniform(0.7, 1.5)
        self.speed_x = random.uniform(0.8, 1.5)
        self.amplitude = random.uniform(50, 100)
        self.frequency = random.uniform(0.01, 0.05)
        self.start_x = x
        self.time = 0
        self.oscillate = random.choice([True, False])
        self.horizontal = random.choice([True, False])
        self.oscillate_start_y = random.randint(HEIGHT // 4, HEIGHT // 2)
        self.dropping = True  # Initial state is dropping down

    def update(self):
        if self.dropping:
            self.rect.y += self.speed_y
            if self.rect.y >= self.target_y:
                self.rect.y = self.target_y
                self.dropping = False  # Stop dropping and start normal behavior
        else:
            if self.horizontal:
                self.rect.x += self.speed_x
                if self.rect.left <= 0 or self.rect.right >= WIDTH:
                    self.speed_x *= -1
            else:
                if self.rect.y < self.oscillate_start_y:
                    self.rect.y += self.speed_y
                else:
                    if self.oscillate:
                        new_x = self.start_x + self.amplitude * math.sin(self.frequency * self.time)
                        if abs(new_x - self.rect.x) > 1:  # Ensure noticeable movement
                            self.rect.x = new_x
                    self.time += 1

            # Ensure the alien ship stays within the screen boundaries
            self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))


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
    global all_sprites, bullets, enemies, alien_ships, explosions, weapon_supplies

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    alien_ships = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    weapon_supplies = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    LEVELS = 3  # Total number of levels
    level = 1   # Current level
    level_score_requirement = 10  
    score = 0
    lives = player.lives

    MAX_ENEMIES_PER_WAVE = 20
    enemies_spawned = 0
    enemies_killed = 0

    weapon_supply_event = pygame.USEREVENT + 3
    pygame.time.set_timer(weapon_supply_event, 3000)  # Adjust the time as needed

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
            elif event.type == weapon_supply_event:
                weapon_supply = WeaponSupply()
                all_sprites.add(weapon_supply)
                weapon_supplies.add(weapon_supply)

        keys = pygame.key.get_pressed()
        player.update(keys)

        for sprite in all_sprites:
            if sprite != player:
                sprite.update()

        # Spawn enemies if needed
        if enemies_spawned < MAX_ENEMIES_PER_WAVE and len(enemies) + len(alien_ships) < MAX_ENEMIES_PER_WAVE:
            enemy_type = random.choice(['enemy', 'alien'])
            if enemy_type == 'enemy':
                enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(-40, HEIGHT // 2 - 40))
                all_sprites.add(enemy)
                enemies.add(enemy)
            else:
                alien_ship = AlienShip(random.randint(0, WIDTH - 40), random.randint(-40, HEIGHT // 2 - 40))
                all_sprites.add(alien_ship)
                alien_ships.add(alien_ship)
            enemies_spawned += 1
            print(f'Enemies spawned: {enemies_spawned}')  # Debug

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 1
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            explosions.add(explosion)
            explosion_sound.play()
            print(f'Enemy killed. Total enemies killed: {enemies_killed}')  # Debug

        alien_hits = pygame.sprite.groupcollide(bullets, alien_ships, True, True)
        for hit in alien_hits:
            score += 2  # Alien ships give more points
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            explosions.add(explosion)
            explosion_sound.play()
            print(f'Alien ship killed. Total enemies killed: {enemies_killed}')  # Debug


        enemy_hits = pygame.sprite.spritecollide(player, enemies, True)
        alien_ship_hits = pygame.sprite.spritecollide(player, alien_ships, True)
        if enemy_hits or alien_ship_hits:
            player.lives -= 1
            lives -= 1
            if player.lives <= 0:
                game_over(score)
 
        supply_hits = pygame.sprite.spritecollide(player, weapon_supplies, True)
        for supply in supply_hits:
            player.bullet_count += 1

        # Check if all enemies have been killed to spawn the next wave
        #print(f'Enemies killed: {enemies_killed} / {MAX_ENEMIES_PER_WAVE}') 
        if (len(enemies) + len(alien_ships)) == 0:
            enemies_spawned = 0
            level += 1

#         for enemy in enemies:
#             if enemy.rect.top > HEIGHT or enemy.rect.right < 0 or enemy.rect.left > WIDTH:
#                 enemy.kill()
#                 enemies_killed += 1
#                 # print(f'Enemy went off-screen. Total enemies killed: {enemies_killed}')  # Debug

#         for alien_ship in alien_ships:
#             if alien_ship.rect.top > HEIGHT or alien_ship.rect.right < 0 or alien_ship.rect.left > WIDTH:
#                 alien_ship.kill()
#                 enemies_killed += 1
#                 print(f'Alien ship went off-screen. Total enemies killed: {enemies_killed}')  # Debug

# # Ensure no enemies or alien ships are left when counting kills
#         print(f'Total enemies on screen: {len(enemies) + len(alien_ships)}')  # Debug

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
                    settings_menu()
                elif exit_btn.collidepoint(mouse_pos):
                    running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
alien_ships = pygame.sprite.Group()

# Start the main menu
main_menu()
