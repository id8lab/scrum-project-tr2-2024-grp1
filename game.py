import pygame
from player import Player
from enemy import Enemy
import random

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(width//2, height - 60)

        # Create enemies
        self.enemies = [Enemy(random.randint(0, width-50), random.randint(-1000, -50)) for _ in range(5)]

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()
            if keys[pygame.K_SPACE]:
                self.player.shoot()

            self.update()
            self.draw()

            self.clock.tick(60)

    def update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
            if enemy.rect.y > self.height:
                enemy.respawn()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        pygame.display.update()
