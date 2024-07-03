import pygame

pygame.init()
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

player_image = pygame.image.load("./assets/player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.image.load("./assets/enemy.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (100, 100))
alien_ship_image = pygame.image.load("./assets/alien_ships.png").convert_alpha()
alien_ship_image = pygame.transform.scale(alien_ship_image, (100, 100))

shooting_sound = pygame.mixer.Sound("./assets/laser.mp3")
shooting_sound.set_volume(0.2)

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
alien_ships = pygame.sprite.Group()
explosions = pygame.sprite.Group()
weapon_supplies = pygame.sprite.Group()