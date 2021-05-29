from bdd import Bdd
import pygame
from projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos, pseudo):
        super().__init__()
        self.game = game
        self.alive = True
        self.pos = pos
        self.pseudo = pseudo
        self.health = 61
        self.max_health = 61
        self.attack = 20
        self.velocity = 1
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/player.png')
        self.image = pygame.transform.scale(self.image, (40,70))
        self.rect = self.image.get_rect()
        self.origin_image = self.image
        self.angle = 0
        self.direction = pygame.math.Vector2(0, 1)
        self.angle_speed = 1
        self.scale = 1.5

        self.bdd = Bdd()
    
    def update_data_player_at_start_when_everyone_are_ready_to_play_the_game(self, table):
        req = self.bdd.select_data_player(table, "*")
        donnees = {}
        for idx,data in enumerate(req):
            donnees[idx] = data
        self.pseudo, self.velocity, self.angle_speed, self.attack, self.health = donnees[1], donnees[2], donnees[3], donnees[4], donnees[5]
        self.max_health = self.health

    def damage(self, amount, target):
        self.health -= amount
        if self.health >= 1:
            target.alive = True
        else:
            self.game.game_over()
            target.alive = False
        return target.alive
    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x, self.rect.y, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x, self.rect.y, self.health, 5])
        
    def shoot(self):
        self.all_projectiles.add(Projectile(self, (self.pos[0], self.pos[1]), (self.direction.x, self.direction.y)))

    def update(self):
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, self.scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def move(self, x_axis, y_axis):
        delta_rot = x_axis*self.angle_speed
        self.angle -= delta_rot

        vec = pygame.math.Vector2(0, 1)
        vec.y = y_axis*self.velocity
        vec.rotate_ip(-self.angle)

        self.direction.rotate_ip(delta_rot)
        self.direction.normalize_ip()

        self.pos = (self.pos[0] + vec.x, self.pos[1] + vec.y)
