import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5
        self.bullets = []

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        bullet = pygame.Rect(self.rect.centerx - 2, self.rect.top - 10, 5, 10)
        self.bullets.append(bullet)

    def update(self):
        for bullet in self.bullets:
            bullet.y -= 10
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for bullet in self.bullets:
            pygame.draw.rect(screen, (255, 0, 0), bullet)
