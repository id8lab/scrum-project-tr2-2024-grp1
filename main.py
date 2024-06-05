import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch the Falling Objects")

# Define the player
player_width = 50
player_height = 50
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Define the falling object
object_width = 30
object_height = 30
object_x = random.randint(0, screen_width - object_width)
object_y = -object_height
object_speed = 5

# Score
score = 0
font = pygame.font.SysFont(None, 36)

def draw_player(x, y):
    pygame.draw.rect(screen, black, [x, y, player_width, player_height])

def draw_object(x, y):
    pygame.draw.rect(screen, red, [x, y, object_width, object_height])

def display_score(score):
    text = font.render(f"Score: {score}", True, black)
    screen.blit(text, [10, 10])

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Update object position
    object_y += object_speed

    # Check if the object is caught
    if (object_y + object_height > player_y and
        object_x + object_width > player_x and
        object_x < player_x + player_width):
        score += 1
        object_x = random.randint(0, screen_width - object_width)
        object_y = -object_height
        object_speed += 1

    # Check if the object is missed
    if object_y > screen_height:
        object_x = random.randint(0, screen_width - object_width)
        object_y = -object_height

    # Fill the screen with white color
    screen.fill(white)

    # Draw player and object
    draw_player(player_x, player_y)
    draw_object(object_x, object_y)

    # Display score
    display_score(score)

    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(30)

pygame.quit()
