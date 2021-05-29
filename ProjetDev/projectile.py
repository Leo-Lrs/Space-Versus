import pygame
from pygame.event import peek

class Projectile(pygame.sprite.Sprite):
    def __init__(self, player, pos, direction):
        super().__init__()
        self.velocity = 1.5
        self.player = player
        self.pos = pos
        self.direction = pygame.math.Vector2(direction[0], direction[1])
        self.image = pygame.image.load('assets/projectile.png')
        self.image = pygame.transform.scale(self.image, (15,15))
        self.rotation = self.direction.angle_to(pygame.math.Vector2(0, 1))
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()

    def update(self, player2, player2_group):
        self.pos = (self.pos[0] - self.velocity*self.direction[0], self.pos[1] - self.velocity*self.direction[1])
        self.rect.center = self.pos
        pygame.sprite.groupcollide(self.player.all_projectiles, player2.all_projectiles, 1, 1)
        state = True
        if pygame.sprite.spritecollideany(self, player2_group) != None:
            self.remove()
            state = player2.damage(self.player.attack, player2)
        if self.rect.x > 1080 or self.rect.x < -10 or self.rect.y < 0 or self.rect.y > 720:
            self.remove()
        return state

    def remove(self):
        self.player.all_projectiles.remove(self)