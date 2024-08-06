import pygame
import sys
import random
import math
import json

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

player_name = ""

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
character_images = []
for i in range(1, 6):
    image = pygame.image.load(f"./assets/character_{i}.png").convert_alpha()
    image = pygame.transform.scale(image, (100, 100))  # Adjust size as needed
    character_images.append(image)

# Set the default player image
current_character_index = 0
player_image = pygame.transform.scale (character_images[current_character_index], (100, 100))
enemy_image = pygame.image.load("./assets/enemy.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (100, 100))
alien_ship_image = pygame.image.load("./assets/alien_ships.png").convert_alpha()
alien_ship_image = pygame.transform.scale(alien_ship_image, (100, 100))

boss_image = pygame.image.load("./assets/enemyboss.png").convert_alpha()
boss_image = pygame.transform.scale(boss_image, (200, 200))  # Adjust the size as needed

# Font
font = pygame.font.Font("./assets/8bit_font.ttf", 74)
button_font = pygame.font.Font("./assets/8bit_font.ttf", 50)
score_font = pygame.font.Font("./assets/8bit_font.ttf", 36)

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
        self.speed = random.uniform(0.5, 0.5)
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
def create_button(text, center_x, center_y, width=300, height=70):
    rect = pygame.Rect(0,0, width, height)
    rect.center = (center_x, center_y)
    text_render = button_font.render(text, True, WHITE)
    text_rect = text_render.get_rect(center=(center_x, center_y))
    rect.size = (width, height)
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)
    screen.blit(text_render, text_rect)
    return rect

# Load weapon supply image
weapon_supply_image = pygame.image.load("./assets/weapon_supply.png").convert_alpha()
weapon_supply_image = pygame.transform.scale(weapon_supply_image, (80, 80))

# File to store scores
import json

SCORES_FILE = 'scores.json'


def save_score(player_name, score):
    new_entry = {"score": score, "player_name": player_name}
    try:
        # Initialize scores list if the file does not exist or is empty
        try:
            with open(SCORES_FILE, 'r') as file:
                scores = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []

        # Append new score and write back
        scores.append(new_entry)
        with open(SCORES_FILE, 'w') as file:
            json.dump(scores, file, indent=4)
        print(f"Score saved: {new_entry}")  # Debug print
    except Exception as e:
        print(f"An error occurred: {e}")


def load_scores():
    try:
        with open(SCORES_FILE, 'r') as file:
            scores = json.load(file)
            # Convert old int scores to the new format if necessary
            converted_scores = []
            for score in scores:
                if isinstance(score, int):
                    converted_scores.append({"score": score, "player_name": "Unknown"})
                else:
                    converted_scores.append(score)
            sorted_scores = sorted(converted_scores, key=lambda x: x['score'], reverse=True)[:5]
            print(f"Scores loaded: {sorted_scores}")  # Debug print
            return sorted_scores
    except (FileNotFoundError, json.JSONDecodeError):
        return []



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


class EnemyBoss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = boss_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_y = random.uniform(0.5, 1.0)
        self.amplitude = random.uniform(30, 80)
        self.frequency = random.uniform(0.01, 0.03)
        self.start_x = x
        self.time = 0
        self.shoot_delay = 1000  # Delay between each shot in milliseconds
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top >= HEIGHT // 4:
            self.speed_y = 0  # Stop moving down once it reaches a certain point

        self.rect.x = self.start_x + self.amplitude * math.sin(self.frequency * self.time)
        self.time += 1

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()

    def shoot(self):
        boss_bullet = BossBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(boss_bullet)
        boss_bullets.add(boss_bullet)
    
class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(midtop=(x, y))
        self.speed_y = 5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

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

class SpriteBase(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, 0))  # Start at the top of the screen
        self.target_y = target_y  # The designated position
        self.speed_y = random.uniform(0.7, 1.5)
        self.speed_x = random.uniform(0.8, 1.5)
        self.amplitude = random.uniform(50, 100)
        self.frequency = random.uniform(0.01, 0.05)
        self.start_x = x
        self.time = 0
        self.horizontal = True
        self.dropping = True  # Initial state is dropping down
        self.square_move = random.choice([True, False])
        self.direction = 'left'  # Initial direction for square movement

    def update(self):
        if self.dropping:
            self.rect.y += self.speed_y
            if self.rect.y >= self.target_y:
                self.rect.y = self.target_y
                self.dropping = False  # Stop dropping and start normal behavior
        else:
            if self.square_move:
                self.move_in_square()
            else:
                if self.horizontal:
                    self.rect.x += self.speed_x
                    if self.rect.left <= 0 or self.rect.right >= WIDTH:
                        self.speed_x *= -1

            # Ensure the sprite stays within the screen boundaries
            self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def move_in_square(self):
        if self.direction == 'left':
            self.rect.x -= self.speed_x
            if self.rect.x <= 0:
                self.rect.x = 0
                self.direction = 'up'
        elif self.direction == 'up':
            self.rect.y -= self.speed_y
            if self.rect.y <= 0:
                self.rect.y = 0
                self.direction = 'right'
        elif self.direction == 'right':
            self.rect.x += self.speed_x
            if self.rect.x >= WIDTH - self.rect.width:
                self.rect.x = WIDTH - self.rect.width
                self.direction = 'down'
        elif self.direction == 'down':
            self.rect.y += self.speed_y
            if self.rect.y >= self.target_y:
                self.rect.y = self.target_y
                self.direction = 'left'

class Enemy(SpriteBase):
    def __init__(self, x, y):
        super().__init__(enemy_image, x, y, y)
        self.circle_move = random.choice([True, False])
        self.radius = random.uniform(100, 200)  # Larger radius for bigger circles
        self.angle = 0
        self.center_x = x
        self.center_y = y

    def update(self):
        super().update()
        if not self.dropping and self.circle_move:
            self.move_in_circle()

    def move_in_circle(self):
        self.angle += self.speed_x * 0.002  # Slower angular speed for circular movement
        self.rect.x = self.center_x + self.radius * math.cos(self.angle)
        self.rect.y = self.center_y + self.radius * math.sin(self.angle)


class AlienShip(SpriteBase):
    def __init__(self, x, y):
        super().__init__(alien_ship_image, x, y, y)




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

def game_over(score):
    player_name = ""  # Initialize player_name here
    base_font = pygame.font.Font("./assets/8bit_font.ttf", 32)  # Font for name input
    prompt_font = pygame.font.Font("./assets/8bit_font.ttf", 36)  # Font for the prompt text

    # Define vertical positions
    input_box_y = HEIGHT // 2 + 50
    name_prompt_y = input_box_y - 40
    button_start_y = HEIGHT // 2 + 150
    vertical_gap = 80

    # Define the input box and prompt
    input_box = pygame.Rect(WIDTH // 2 - 100, input_box_y, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    input_active = False

    # Timer for cursor blinking
    cursor_blink_timer = pygame.time.get_ticks()
    cursor_blink_interval = 500  # Cursor blinks every 500 milliseconds

    # Load scores and determine rank
    scores = load_scores()
    current_rank = None
    if scores:
        # Corrected line
        sorted_scores = sorted(scores + [{"player_name": "current", "score": score}], key=lambda x: x['score'], reverse=True)
        current_rank = sorted_scores.index({"player_name": "current", "score": score}) + 1

    running = True
    while running:
        screen.fill((0, 0, 0))

        for star in stars:
            star.move()
            star.draw(screen)

        settings_text = font.render("GAME OVER", True, WHITE)
        settings_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(settings_text, settings_rect)

        score_text = font.render(f"Your Score is {score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 70))
        screen.blit(score_text, score_rect)

        if current_rank is not None:
            rank_text = font.render(f"Your Rank is {current_rank}", True, YELLOW)
            rank_rect = rank_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 150))
            screen.blit(rank_text, rank_rect)

        # Adjust position of name input prompt and box
        name_prompt = prompt_font.render("Enter your name:", True, WHITE)
        name_prompt_rect = name_prompt.get_rect(center=(WIDTH // 2, name_prompt_y))  # Center horizontally
        screen.blit(name_prompt, name_prompt_rect)
        pygame.draw.rect(screen, color, input_box, 2)

        # Render the player_name
        name_surface = base_font.render(player_name, True, WHITE)
        screen.blit(name_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(200, name_surface.get_width() + 10)

        # Cursor blinking logic
        now = pygame.time.get_ticks()
        if not input_active and not player_name and (now - cursor_blink_timer) % (2 * cursor_blink_interval) < cursor_blink_interval:
            cursor_x = input_box.x + name_surface.get_width() + 5
            cursor_y = input_box.y + 5
            pygame.draw.line(screen, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + 24), 2)

        # Adjust button positions
        cont_btn = create_button("Continue", WIDTH // 2, button_start_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                    color = color_active
                else:
                    input_active = False
                    color = color_inactive

                mouse_pos = event.pos
                if cont_btn.collidepoint(mouse_pos):
                    if player_name:  # Save only if name is entered
                        save_score(player_name, score)
                        game_over_menu(score)
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if player_name:  # Save only if name is entered
                            save_score(player_name, score)
                        input_active = False
                        color = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        pygame.display.flip()


def game_over_menu(score):
    player_name = ""  # Initialize player_name here
    base_font = pygame.font.Font("./assets/8bit_font.ttf", 32)  # Font for name input
    prompt_font = pygame.font.Font("./assets/8bit_font.ttf", 36)  # Font for the prompt text

    # Define vertical positions
    input_box_y = HEIGHT // 2 + 50
    name_prompt_y = input_box_y - 40
    button_start_y = HEIGHT // 2 + 150
    vertical_gap = 80

    # Define the input box and prompt
    input_box = pygame.Rect(WIDTH // 2 - 100, input_box_y, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    input_active = False

    # Timer for cursor blinking
    cursor_blink_timer = pygame.time.get_ticks()
    cursor_blink_interval = 500  # Cursor blinks every 500 milliseconds

    # Load scores and determine rank
    scores = load_scores()
    current_rank = None
    if scores:
        # Corrected line
        sorted_scores = sorted(scores + [{"player_name": "current", "score": score}], key=lambda x: x['score'], reverse=True)
        current_rank = sorted_scores.index({"player_name": "current", "score": score}) + 1

    running = True
    while running:
        screen.fill((0, 0, 0))

        for star in stars:
            star.move()
            star.draw(screen)

        settings_text = font.render("GAME OVER", True, WHITE)
        settings_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(settings_text, settings_rect)

        score_text = font.render(f"Your Score is {score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 70))
        screen.blit(score_text, score_rect)

        if current_rank is not None:
            rank_text = font.render(f"Your Rank is {current_rank}", True, YELLOW)
            rank_rect = rank_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 150))
            screen.blit(rank_text, rank_rect)

  


        # Adjust button positions
        replay_btn = create_button("Replay", WIDTH // 2, button_start_y)
        scores_btn = create_button("Scores", WIDTH // 2, button_start_y + vertical_gap)
        exit_btn = create_button("Exit", WIDTH // 2, button_start_y + 2 * vertical_gap)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                    color = color_active
                else:
                    input_active = False
                    color = color_inactive

                mouse_pos = event.pos
                if replay_btn.collidepoint(mouse_pos):
                    main_game()
                elif scores_btn.collidepoint(mouse_pos):
                    high_scores_screen()
                elif exit_btn.collidepoint(mouse_pos):
                    if player_name:  # Save only if name is entered
                        save_score(player_name, score)
                    main_menu()
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if player_name:  # Save only if name is entered
                            save_score(player_name, score)
                        input_active = False
                        color = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        pygame.display.flip()


def high_scores_screen():
    try:
        retro_font = pygame.font.Font("./assets/8bit_font.ttf", 36)  # Increased font size
    except:
        retro_font = pygame.font.Font(None, 36)  # Fallback if custom font fails

    # Load crown image
    crown_image = pygame.image.load("./assets/crown.png").convert_alpha()
    crown_image = pygame.transform.scale(crown_image, (35, 35))  # Slightly larger crown

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    scores = load_scores()

    running = True
    while running:
        screen.blit(background, (0, 0))

        title_text = retro_font.render("Galaxia HIGH SCORES", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 8))
        screen.blit(title_text, title_rect)

        # Measure text width for centering
        player_width = retro_font.size("PLAYER")[0]
        score_width = retro_font.size("SCORE")[0]

        # Calculate columns' positions
        column_spacing = 100  # Space between the columns
        player_column_x = (WIDTH - (player_width + score_width + column_spacing)) // 2
        score_column_x = player_column_x + player_width + column_spacing

        # Draw column titles
        player_title = retro_font.render("PLAYER", True, (0, 255, 255))
        score_title = retro_font.render("SCORE", True, (0, 255, 255))
        screen.blit(player_title, (player_column_x, HEIGHT // 4))
        screen.blit(score_title, (score_column_x, HEIGHT // 4))

        # List scores
        for i, score in enumerate(scores):
            y = HEIGHT // 4 + 50 * (i + 1)  # Adjusted for larger font
            player_text = retro_font.render(str(score["player_name"]), True, (0, 255, 255))
            score_text = retro_font.render(str(score["score"]), True, YELLOW)
            screen.blit(player_text, (player_column_x, y))
            screen.blit(score_text, (score_column_x, y))

            # Draw crown for top scorer
            if i == 0:
                screen.blit(crown_image, (player_column_x - 50, y - 10))  # More left, adjusted position

        # Create "Back" button
        exit_btn = create_button("Back", WIDTH // 2, HEIGHT // 2 + 300)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if exit_btn.collidepoint(mouse_pos):
                    running = False
        
        pygame.display.flip()



def multiplayer_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))

        for star in stars:
            star.move()
            star.draw(screen)

        settings_text = font.render("MULTIPLAYER", True, WHITE)
        settings_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(settings_text, settings_rect)

        vertical_gap = 80
        server_btn = create_button("Server", WIDTH // 2, HEIGHT // 2)
        client_btn = create_button("Client", WIDTH // 2, HEIGHT // 2 + vertical_gap)
        exit_btn = create_button("Back", WIDTH // 2, HEIGHT // 2 + 2 * vertical_gap)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if server_btn.collidepoint(mouse_pos):
                    print("server")
                elif client_btn.collidepoint(mouse_pos):
                    print("client")
                elif exit_btn.collidepoint(mouse_pos):
                    main_menu()

        pygame.display.flip()


def pause_menu(current_score):
    running = True
    player_name = ""  # Initialize player_name here
    base_font = pygame.font.Font("./assets/8bit_font.ttf", 32)  # Font for name input
    prompt_font = pygame.font.Font("./assets/8bit_font.ttf", 36)  # Font for the prompt text

    # Define vertical positions
    input_box_y = HEIGHT // 2 + 50
    name_prompt_y = input_box_y - 40
    button_start_y = HEIGHT // 2 + 100
    vertical_gap = 80

    # Define the input box and prompt
    input_box = pygame.Rect(WIDTH // 2 - 100, input_box_y, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    input_active = False

    cursor_blink_timer = pygame.time.get_ticks()
    cursor_blink_interval = 500  # Cursor blinks every 500 milliseconds

    # Load scores and determine rank
    scores = load_scores()
    current_rank = None
    if scores:
        sorted_scores = sorted(scores + [{"player_name": "current", "score": current_score}], key=lambda x: x['score'], reverse=True)
        current_rank = sorted_scores.index({"player_name": "current", "score": current_score}) + 1

    while running:
        screen.fill((0, 0, 0))

        for star in stars:
            star.move()
            star.draw(screen)

        settings_text = font.render("PAUSE", True, WHITE)
        settings_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(settings_text, settings_rect)

        score_text = font.render(f"Your Score is {current_score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 70))
        screen.blit(score_text, score_rect)


        # Adjust button positions
        resume_btn = create_button("Resume", WIDTH // 2, button_start_y)
        # settings_btn = create_button("Settings", WIDTH // 2, button_start_y + 1 * vertical_gap)
        exit_btn = create_button("Exit", WIDTH // 2, button_start_y + 1 * vertical_gap)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = not input_active
                else:
                    input_active = False
                color = color_active if input_active else color_inactive
                mouse_pos = event.pos
                if resume_btn.collidepoint(mouse_pos):
                    running = False
                elif exit_btn.collidepoint(mouse_pos):
                    if player_name:
                        save_score(player_name, current_score)
                    main_menu()
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if player_name:  # Save only if name is entered
                            save_score(player_name, current_score)
                        input_active = False
                        color = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        pygame.display.flip()


def main_game():
    global all_sprites, bullets, enemies, alien_ships, explosions, weapon_supplies, boss_bullets, boss

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    alien_ships = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    weapon_supplies = pygame.sprite.Group()
    boss_bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    LEVELS = 3  # Total number of levels
    level = 1   # Current level
    score = 0
    lives = player.lives

    MAX_ENEMIES_PER_WAVE = 20
    enemies_spawned = 0
    enemies_killed = 0

    boss_died = True
    boss_hit_count = 0

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
                    pause_menu(score)
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
        if enemies_spawned < MAX_ENEMIES_PER_WAVE and len(enemies) + len(alien_ships) < MAX_ENEMIES_PER_WAVE and boss_died:
            enemy_type = random.choice(['enemy', 'alien'])
            boss = EnemyBoss(WIDTH // 2 - 100, -200)
            if enemy_type == 'enemy':
                enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(-40, HEIGHT // 2 - 40))
                all_sprites.add(enemy)
                enemies.add(enemy)
            else:
                alien_ship = AlienShip(random.randint(0, WIDTH - 40), random.randint(-40, HEIGHT // 2 - 40))
                all_sprites.add(alien_ship)
                alien_ships.add(alien_ship)
            enemies_spawned += 1
            if (len(enemies) + len(alien_ships)) ==  20:
                boss_hit_count = 0
                all_sprites.add(boss)
                boss_died = False

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

        if not boss_died:
            boss_killed = pygame.sprite.spritecollide(boss, bullets, True)
            if boss_killed:
                boss_hit_count += 1  
                if boss_hit_count > 5:
                    for hit in boss_killed:
                        score += 10 
                        explosion = Explosion(hit.rect.centerx, hit.rect.centery)
                        all_sprites.add(explosion)
                        explosions.add(explosion)
                        explosion_sound.play()
                        boss.kill()
                        boss_died = True


        enemy_hits = pygame.sprite.spritecollide(player, enemies, True)
        alien_ship_hits = pygame.sprite.spritecollide(player, alien_ships, True)
        if enemy_hits or alien_ship_hits:
            player.lives -= 1
            lives -= 1
            if player.lives <= 0:
                game_over(score)
                return  # Exit the function to avoid continuing after game over

        supply_hits = pygame.sprite.spritecollide(player, weapon_supplies, True)
        for supply in supply_hits:
            player.bullet_count += 1
        

        boss_hits = pygame.sprite.spritecollide(player, boss_bullets, True)
        if boss_hits:
            player.lives -= 1
            lives -= 1
            if player.lives <= 0:
                game_over(score)

        if (len(enemies) + len(alien_ships)) == 0:
            enemies_spawned = 0
            if(boss_died):
                level+=1


        # Drawing
        screen.fill((0, 0, 0))
        for star in stars:
            star.move()
            star.draw(screen)

        all_sprites.draw(screen)

        score_text = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        lives_text = score_font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (WIDTH - 120, 10))

        # Display current level
        level_text = score_font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (WIDTH // 2 - 50, 10))

        pygame.display.flip()

def main_menu():
    global player_name
    running = True
    input_active = False
    title_font = pygame.font.Font("./assets/8bit_font.ttf", 72)
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 4 + 140, 300, 50) 

    while running:
        screen.fill((0, 0, 0))

        # Title
        title_text = title_font.render("Galaxia", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # # Input label
        # label_text = font.render("Enter your name", True, WHITE)
        # label_rect = label_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 90))
        # screen.blit(label_text, label_rect)

        # # Input box
        

        # Display buttons only if player_name has at least 2 characters
        vertical_gap = 100
        single_player_btn = create_button("Single Player", WIDTH // 2, HEIGHT // 2)
        multiplayer_btn = create_button("Multiplayer", WIDTH // 2, HEIGHT // 2 + vertical_gap)
        scores_btn = create_button("Scores", WIDTH // 2, HEIGHT // 2 + 2 * vertical_gap)
        settings_btn = create_button("Settings", WIDTH // 2, HEIGHT // 2 + 3 * vertical_gap)
        exit_btn = create_button("Exit", WIDTH // 2, HEIGHT // 2 + 4 * vertical_gap)

            # Handle button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False

                mouse_pos = event.pos
                if single_player_btn.collidepoint(mouse_pos):
                    main_game()
                elif multiplayer_btn.collidepoint(mouse_pos):
                    multiplayer_menu()
                elif scores_btn.collidepoint(mouse_pos):
                    high_scores_screen()
                elif settings_btn.collidepoint(mouse_pos):
                    settings_menu()
                elif exit_btn.collidepoint(mouse_pos):
                    running = False
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        else:
            # Handle input events only when player_name has less than 2 characters
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        input_active = True
                    else:
                        input_active = False
                elif event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        else:
                            player_name += event.unicode

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# Start the main menu
main_menu()