from utils import player_image, WIDTH, HEIGHT, shooting_sound, all_sprites, bullets, pygame
from bullet import Bullet

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