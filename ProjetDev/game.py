import pygame
import time
from datetime import datetime, timedelta
from player import Player
from pygame.locals import *
from menu import *
from bdb import Bdb



class Game:
    def __init__(self, screen):
        self.bdd = Bdd()
        self.screen = screen
        self.screen_dimension = (screen.get_width(), screen.get_height())
        self.player_bords = [[20, self.screen_dimension[0] - 20], [20, self.screen_dimension[1] - 20]]
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.player1_group = pygame.sprite.Group()
        self.player2_group = pygame.sprite.Group()
        self.pressed = {
        }

        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False
        self.UP_KEY2, self.DOWN_KEY2, self.START_KEY2, self.BACK_KEY2, self.RIGHT_KEY2, self.LEFT_KEY2 = False, False, False, False, False, False
        self.list_keys = [
            [self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY],
            [self.UP_KEY2, self.DOWN_KEY2, self.START_KEY2, self.BACK_KEY2, self.RIGHT_KEY2, self.LEFT_KEY2]
        ]
        self.display = pygame.Surface((self.screen_dimension[0],self.screen_dimension[1]))
        self.window = pygame.display.set_mode(((self.screen_dimension[0],self.screen_dimension[1])))
        self.font_name = 'assets/typo/spaceage.ttf'
        self.BLACK, self.WHITE, self.COLORTEST = (0, 0, 0), (255, 255, 255), (57, 167, 218)
        self.main_menu = MainMenu(self)
        self.instructions = InstructionsMenu(self)
        self.score = ScoreMenu(self)
        self.ig_settings = ConfigGame(self)
        self.curr_menu = self.main_menu

    def calcul_score(self, player1, player2, timer):
        if player1.alive == True:
            winner = player1
            looser = player2
            pseudo = winner.pseudo
        elif player2.alive == True:
            winner = player2
            looser = player1
            pseudo = winner.pseudo
            
        point_vie = winner.health * 100
        
        point_timer = 1000 - timer

        point_rotation = looser.angle_speed - winner.angle_speed
        if point_rotation > 0 and point_rotation <= 5:
            point_rotation = 100*2
        elif point_rotation > 5 and point_rotation < 10 :
            point_rotation = 100*3
        elif point_rotation == 0:
            point_rotation = 100
        elif point_rotation < 0:
            point_rotation = 50 

        point_vitesse = looser.velocity - winner.velocity
        if point_vitesse > 0:
            point_vitesse = 100*2
        elif point_vitesse > 5 and point_vitesse < 10 :
            point_vitesse = 100*5
        elif point_vitesse == 0:
            point_vitesse = 100
        elif point_vitesse < 0:
            point_vitesse = 50   

        point_attack = looser.attack -  winner.attack
        if point_attack > 0:
            point_attack = 100*2
        elif point_attack > 5 and point_attack < 10 :
            point_attack = 100*3
        elif point_attack == 0:
            point_attack = 100
        elif point_attack < 0:
            point_attack = 50
        


        score = point_vie + point_rotation + point_vitesse + point_attack + point_timer
    
        self.bdd.update_score(pseudo, score)  
        
        return score, pseudo

    def check_events(self):

        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for idx, key in enumerate(self.list_keys):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running, self.playing = False, False
                    self.curr_menu.run_display = False
                    pygame.quit()
                    print("Fermeture du jeu")
                if event.type == pygame.JOYAXISMOTION:
                    if pygame.joystick.Joystick(idx).get_axis(1) < -0.1:
                        self.list_keys[idx][0] = True
                        if idx == 0:
                            self.UP_KEY = True
                        else:
                            self.UP_KEY2 = True
                    if pygame.joystick.Joystick(idx).get_axis(1) > 0.1:
                        self.list_keys[idx][1] = True
                        if idx == 0:
                            self.DOWN_KEY = True
                        else:
                            self.DOWN_KEY2 = True
                    if pygame.joystick.Joystick(idx).get_axis(0) > 0.5:
                        self.list_keys[idx][4] = True
                        if idx == 0:
                            self.RIGHT_KEY = True
                        else:
                            self.RIGHT_KEY2 = True
                    if pygame.joystick.Joystick(idx).get_axis(0) < -0.5:
                        self.list_keys[idx][5] = True
                        if idx == 0:
                            self.LEFT_KEY = True
                        else:
                            self.LEFT_KEY2 = True
                if event.type == pygame.JOYBUTTONDOWN:
                    if pygame.joystick.Joystick(idx).get_button(0) == 1:
                        self.list_keys[idx][2] = True
                        if idx == 0:
                            self.START_KEY = True
                        else:
                            self.START_KEY2 = True
                    if pygame.joystick.Joystick(idx).get_button(1) == 1:
                        self.list_keys[idx][3] = True
                        if idx == 0:
                            self.BACK_KEY = True
                        else:
                            self.BACK_KEY2 = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False
        self.UP_KEY2, self.DOWN_KEY2, self.START_KEY2, self.BACK_KEY2, self.RIGHT_KEY2, self.LEFT_KEY2 = False, False, False, False, False, False
        self.list_keys = [
            [self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY],
            [self.UP_KEY2, self.DOWN_KEY2, self.START_KEY2, self.BACK_KEY2, self.RIGHT_KEY2, self.LEFT_KEY2]
        ]
    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.COLORTEST)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def draw_image(self, file, pos, size):
        image = pygame.image.load(file)
        image = pygame.transform.scale(image, size)
        self.display.blit(image, pos)

    def check_Timer(self):
        return datetime.now()

    def start(self):
        self.is_playing = True
        self.player1 = Player(self, (900, 280), "aaa")
        self.bdd.insert_data_player("player1", self.player1)
        self.player2 = Player(self, (100, 370), "bbb")
        self.bdd.insert_data_player("player2", self.player2)
        self.all_players.add(self.player1)
        self.all_players.add(self.player2)
        self.player1_group.add(self.player1)
        self.player2_group.add(self.player2)
        self.player1.rect.center = self.player1.pos
        self.player2.rect.center = self.player2.pos
        self.player1.update_data_player_at_start_when_everyone_are_ready_to_play_the_game("player1")
        self.player2.update_data_player_at_start_when_everyone_are_ready_to_play_the_game("player2")
        self.time_start = self.check_Timer()
    
    def game_over(self):
        self.total_time = self.check_Timer()- self.time_start
        self.total_time = round(self.total_time.total_seconds())
        self.player1.all_projectiles = pygame.sprite.Group()
        self.player2.all_projectiles = pygame.sprite.Group()
        for player in self.all_players:
            if player.health <= 0:
                player.alive = False
            player.health = player.max_health
        self.is_playing = False
        self.curr_menu = EndGameMenu(self, self.player1, self.player2)

    def draw(self):
        self.screen.blit(self.player1.image, self.player1.rect)
        self.screen.blit(self.player2.image, self.player2.rect)

    def update(self, screen):
        self.player1.all_projectiles.draw(screen)
        self.player2.all_projectiles.draw(screen)
        self.player1.update()
        self.player2.update()
        self.draw()
        for projectile in self.player1.all_projectiles:
            projectile.update(self.player2, self.player2_group)
        for projectile in self.player2.all_projectiles:
            projectile.update(self.player1, self.player1_group)      
        self.player1.update_health_bar(screen)
        self.player2.update_health_bar(screen)

    def manage_joystick(self):
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        vector = [0, 0]
        if pygame.joystick.Joystick(0).get_axis(0) > 0.1:
            vector[0] += 0.4
            self.player1.move(vector[0], vector[1])
        if pygame.joystick.Joystick(0).get_axis(0) < -0.1:
            vector[0] -= 0.4
            self.player1.move(vector[0], vector[1])
        if pygame.joystick.Joystick(0).get_axis(1) < -0.1:
            vector[1] -= 1
            self.player1.move(vector[0], vector[1])
        if pygame.joystick.Joystick(0).get_axis(1) > 0.1:
            vector[1] += 1
            self.player1.move(vector[0], vector[1])

        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(0).get_button(0) == 1:
                    self.player1.shoot()
                if pygame.joystick.Joystick(1).get_button(0) == 1:
                    self.player2.shoot()
                    
        vector = [0, 0]
        if pygame.joystick.Joystick(1).get_axis(0) > 0.1:
            vector[0] += 0.4
            self.player2.move(vector[0], vector[1])
        if pygame.joystick.Joystick(1).get_axis(0) < -0.1:
            vector[0] -= 0.4
            self.player2.move(vector[0], vector[1])
        if pygame.joystick.Joystick(1).get_axis(1) < -0.1:
            vector[1] -= 1
            self.player2.move(vector[0], vector[1])
        if pygame.joystick.Joystick(1).get_axis(1) > 0.1:
            vector[1] += 1
            self.player2.move(vector[0], vector[1])


    def manage_pressed_keys(self):
        pressed = pygame.key.get_pressed()

        #deplacementp1
        vector = [0, 0]
        if pressed[K_RIGHT]:
            vector[0] += 1
            self.player1.move(vector[0], vector[1])
        if pressed[K_LEFT]:
            vector[0] -= 1
            self.player1.move(vector[0], vector[1])
        if pressed[K_UP]:
            vector[1] -= 1
            self.player1.move(vector[0], vector[1])
        if pressed[K_DOWN]:
            vector[1] += 1
            self.player1.move(vector[0], vector[1])

        #deplacementp2
        vector = [0, 0]
        if pressed[K_d]:
            vector[0] += 1
            self.player2.move(vector[0], vector[1])
        if pressed[K_q]:
            vector[0] -= 1
            self.player2.move(vector[0], vector[1])
        if pressed[K_z]:
            vector[1] -= 1
            self.player2.move(vector[0], vector[1])
        if pressed[K_s]:
            vector[1] += 1
            self.player2.move(vector[0], vector[1])
        
        if self.player1.pos[0] < self.player_bords[0][0]:
            self.player1.pos = (self.player_bords[0][0], self.player1.pos[1])
        elif self.player1.pos[0] > self.player_bords[0][1]:
            self.player1.pos = (self.player_bords[0][1], self.player1.pos[1])
        
        if self.player1.pos[1] < self.player_bords[1][0]:
            self.player1.pos = (self.player1.pos[0], self.player_bords[1][0])
        elif self.player1.pos[1] > self.player_bords[1][1]:
            self.player1.pos = (self.player1.pos[0], self.player_bords[1][1])
        
        if self.player2.pos[0] < self.player_bords[0][0]:
            self.player2.pos = (self.player_bords[0][0], self.player2.pos[1])
        elif self.player2.pos[0] > self.player_bords[0][1]:
            self.player2.pos = (self.player_bords[0][1], self.player2.pos[1])
        
        if self.player2.pos[1] < self.player_bords[1][0]:
            self.player2.pos = (self.player2.pos[0], self.player_bords[1][0])
        elif self.player2.pos[1] > self.player_bords[1][1]:
            self.player2.pos = (self.player2.pos[0], self.player_bords[1][1])
        

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
                    