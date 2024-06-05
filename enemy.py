import pygame
import random

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def respawn(self):
        self.rect.x = random.randint(0, 800 - self.rect.width)
        self.rect.y = random.randint(-1000, -50)
