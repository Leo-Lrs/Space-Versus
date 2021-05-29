from player import Player
from sqlite3.dbapi2 import connect
import pygame, string
from bdd import Bdd

class Menu():
    def __init__(self, game):
        self.game = game
        self.bdd = Bdd()
        self.mid_w, self.mid_h = self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.cursor_rect2 = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self, x, y, rect2 = False):
        if rect2:
            self.game.draw_text('*', 30, self.cursor_rect.x - x, self.cursor_rect.y + y)
            self.game.draw_text('*', 30, self.cursor_rect2.x , self.cursor_rect2.y )
        else:
            self.game.draw_text('*', 30, self.cursor_rect.x - x, self.cursor_rect.y + y)



    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.namex, self.namey = self.mid_w, self.mid_h
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.instructionsx, self.instructionsy = self.mid_w, self.mid_h + 50
        self.scorex, self.scorey = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()

            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Space versus', 90, self.namex, self.namey - 180)
            self.game.draw_text('Main Menu', 40, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 40)
            self.game.draw_text("Start Game", 30, self.startx, self.starty+5)
            self.game.draw_text("Instructions", 30, self.instructionsx, self.instructionsy+5)
            self.game.draw_text("Score", 30, self.scorex, self.scorey+5)
            self.draw_cursor(50, 9)
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.instructionsx + self.offset, self.instructionsy)
                self.state = 'Instructions'
            elif self.state == 'Instructions':
                self.cursor_rect.midtop = (self.scorex + self.offset, self.scorey)
                self.state = 'Score'
            elif self.state == 'Score':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.scorex + self.offset, self.scorey)
                self.state = 'Score'
            elif self.state == 'Instructions':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Score':
                self.cursor_rect.midtop = (self.instructionsx + self.offset, self.instructionsy)
                self.state = 'Instructions'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.curr_menu = ConfigGame(self.game)
            elif self.state == 'Instructions':
                self.game.curr_menu = InstructionsMenu(self.game)
            elif self.state == 'Score':
                self.game.curr_menu = ScoreMenu(self.game)
            self.run_display = False
            
class ConfigGame(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.cursor_state1 = "Pseudo"
        self.cursor_state2 = "Pseudo"
        self.is_ready = False
        self.list_setting_p1=[["pseudo"], ["velocity"], ["angle_speed"], ["attack"], ["health"],["valider"]]
        self.list_setting_p2=[["pseudo"], ["velocity"], ["angle_speed"], ["attack"], ["health"],["valider"]]
        self.startx, self.starty = self.game.screen_dimension[0] / 2 - 150, self.game.screen_dimension[1] / 2 - 0 + 20
        self.startx2, self.starty2 = self.game.screen_dimension[0] / 2 + 400, self.game.screen_dimension[1] / 2 - 0 + 20
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty) 
        self.cursor_rect2.midtop = (self.startx2 + self.offset, self.starty2)
        self.cursor_list = [self.cursor_state1, self.cursor_state2]
        self.cursor1 = self.draw_cursor(0, 0, True)

    def cursor_pixel(self):
        self.move_cursor(self.cursor_rect, self.list_setting_p1, "Pseudo", 0)
        self.move_cursor(self.cursor_rect2, self.list_setting_p2, "Pseudo", 1)
        

    
    def move_cursor(self, cursor, list, cursor_state, idx):
        if self.game.list_keys[idx][1]:
            if cursor_state == 'Pseudo':
                cursor.midtop = (list[1][0] + self.offset, list[1][1])
                cursor_state = 'Velocity'
                self.cursor_list[idx] = cursor_state

            elif cursor_state == 'Velocity':
                cursor.midtop = (list[2][0] + self.offset, list[2][1])
                cursor_state = 'Angle_speed'
                self.cursor_list[idx] = cursor_state

            elif cursor_state == 'Angle_speed':
                cursor.midtop = (list[3][0] + self.offset, list[3][1])
                cursor_state = 'Attack'
                self.cursor_list[idx] = cursor_state
            elif cursor_state == 'Attack':
                cursor.midtop = (list[4][0] + self.offset, list[4][1])
                cursor_state = 'Health'
                self.cursor_list[idx] = cursor_state

            elif cursor_state == 'Health':
                cursor.midtop = (list[5][0] + self.offset, list[5][1])
                cursor_state = 'Valider'
                self.cursor_list[idx] = cursor_state

            elif cursor_state == 'Valider':
                cursor.midtop = (list[0][0] + self.offset, list[0][1])
                cursor_state = 'Pseudo'
                self.cursor_list[idx] = cursor_state

        elif self.game.list_keys[idx][0]:
            if cursor_state == 'Pseudo':
                cursor.midtop = (list[5][0] + self.offset, list[5][1])
                cursor_state = 'Valider'
                self.cursor_list[idx] = cursor_state

            elif cursor_state == 'Velocity':
                cursor.midtop = (list[0][0] + self.offset, list[0][1])
                cursor_state = 'Pseudo'
                self.cursor_list[idx] = cursor_state

            elif cursor_state == 'Angle_speed':
                cursor.midtop = (list[1][0] + self.offset, list[1][1])
                cursor_state = 'Velocity'
                self.cursor_list[idx] = cursor_state

            elif cursor_state == 'Attack':
                cursor.midtop = (list[2][0] + self.offset, list[2][1])
                cursor_state = 'Angle_speed'
                self.cursor_list[idx] = cursor_state

            elif cursor_state == 'Health':
                cursor.midtop = (list[3][0] + self.offset, list[3][1])
                cursor_state = 'Attack'
                self.cursor_list[idx] = cursor_state

            elif cursor_state == 'Valider':
                cursor.midtop = (list[4][0] + self.offset, list[4][1])
                cursor_state = 'Health'
                self.cursor_list[idx] = cursor_state


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('In-Game Settings :', 50, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 250)
            y = 0
            i = 0
            donnees = self.bdd.select_data_player("player1", "*")
            self.game.draw_text("Player 1", 35, self.game.screen_dimension[0] / 2 - 150, self.game.screen_dimension[1] / 2 - 150)
            self.game.draw_text("Player 2", 35, self.game.screen_dimension[0] / 2 + 150, self.game.screen_dimension[1] / 2 - 150)
            self.game.draw_text("PLAY", 35, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 + 200)
            self.list_setting_p1[5] = self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 + 200
            self.list_setting_p2[5] = self.game.screen_dimension[0] / 2 + 220, self.game.screen_dimension[1] / 2 + 200
            self.game.draw_text("Pseudo", 25, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 + 20)
            self.game.draw_text("Speed", 25, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 + 40)
            self.game.draw_text("Rotation", 25, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 + 60)
            self.game.draw_text("Attack", 25, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 + 80)
            self.game.draw_text("Health", 25, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 + 100)
            for idx,data in enumerate(donnees):
                if idx != 0:
                    self.game.draw_text(f"{data}", 25, self.game.screen_dimension[0] / 2 - 150, self.game.screen_dimension[1] / 2 - y + 20)
                    self.list_setting_p1[i] = self.game.screen_dimension[0] / 2 - 150, self.game.screen_dimension[1] / 2 - y + 20
                    y -= 20
                    i += 1

            y = 0
            donnees = self.bdd.select_data_player("player2", "*")
            i = 0
            for idx,data in enumerate(donnees):
                if idx != 0:
                    self.game.draw_text(f"{data}", 25, self.game.screen_dimension[0] / 2 + 150, self.game.screen_dimension[1] / 2 - y + 20)
                    self.list_setting_p2[i] = self.game.screen_dimension[0] / 2 + 400, self.game.screen_dimension[1] / 2 - y + 20
                    y -=20
                    i += 1
            if self.is_ready == True:
                break
            self.cursor1 = self.draw_cursor(0, 0, True)
            self.blit_screen()
        
    def check_input(self):
        for event in pygame.event.get():
            for idx, cursor_state in enumerate(self.cursor_list):

                if idx == 0:
                    cursor_rect = self.cursor_rect
                    list_setting = self.list_setting_p1
                    table = "player2"
                if idx == 1:
                    cursor_rect = self.cursor_rect2
                    list_setting = self.list_setting_p2
                    table = "player1"
                
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.JOYBUTTONDOWN:
                    if pygame.joystick.Joystick(0).get_button(0) == 1 and self.cursor_list[0] == "Valider" and self.cursor_list[1] == "Valider":
                        self.is_ready = True
                        self.game.start()
                    if pygame.joystick.Joystick(0).get_button(1) == 1:
                        self.game.curr_menu = self.game.main_menu
                        self.run_display = False
                    if pygame.joystick.Joystick(0).get_button(0) == 1 and self.cursor_list[0] == "Pseudo":
                        info = "Player1"
                        self.game.curr_menu = PseudoEdit(self.game, info)
                        self.run_display = False
                    if pygame.joystick.Joystick(1).get_button(0) == 1 and self.cursor_list[1] == "Pseudo":
                        info = "Player2"
                        self.game.curr_menu = PseudoEdit(self.game, info)
                        self.run_display = False
                if event.type == pygame.JOYAXISMOTION:
                    instance = (0 if idx == 1 else 1)
                    if  event.dict['axis'] == 1 and round(event.dict['value']) == -1 and event.dict['instance_id'] == instance:
                        self.game.list_keys[idx][0] = True
                        self.move_cursor(cursor_rect, list_setting, self.cursor_list[idx], idx)
                    if  event.dict['axis'] == 1 and round(event.dict['value']) == 1 and event.dict['instance_id'] == instance:
                        self.game.list_keys[idx][1] = True
                        self.move_cursor(cursor_rect, list_setting, self.cursor_list[idx], idx)

            if event.type == pygame.JOYAXISMOTION:
                self.gestion_menu(event, 1, 0, "player2")
                self.gestion_menu(event, 0, 1, "player1")


    def gestion_menu(self, event, idx, instance_id, player):
        if event.dict['axis'] == 0 and round(event.dict['value']) == 1 and event.dict['instance_id'] == instance_id:
            if (self.cursor_list[idx] != "Valider" and self.cursor_list[idx] != "Pseudo"):
                self.game.list_keys[idx][4] = True
                
                self.bdd.update_data_player(player, self.cursor_list[idx], 1)

        if event.dict['axis'] == 0 and round(event.dict['value']) == -1 and event.dict['instance_id'] == instance_id:
            if (self.cursor_list[idx] != "Valider" and self.cursor_list[idx] != "Pseudo"):
                self.game.list_keys[idx][5] = True
                
                self.bdd.update_data_player(player, self.cursor_list[idx], -1)


class InstructionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Instructions', 40, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 250)
            self.game.draw_image('assets/InstructionButton.png', (100,150), (500,500))
            self.game.draw_image('assets/InstructionStick.png', (500,150), (500,500))
            self.blit_screen()


class ScoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Top 30 :', 40, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 250)
            
            donnee = self.bdd.hall_of_fame(30)
            y = 200
            for score in donnee:
                self.game.draw_text(f"{score[0]} {score[1]}", 20, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - y)
                y -=20
            self.blit_screen()

class EndGameMenu(Menu):
    def __init__(self, game, player1, player2):
        Menu.__init__(self, game)
        self.player1 = player1
        self.player2 = player2
        self.new_score, self.pseudo = self.game.calcul_score(self.player1, self.player2, self.game.total_time)


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Game is Over', 40, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 250)
            self.game.draw_text(f'Congrats {self.pseudo} You Win', 30, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 175)
            self.game.draw_text('Your score is :', 30, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 125)
            self.game.draw_text(str(self.new_score), 30, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 75)
            self.game.draw_text("Top 10 :", 30, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 25)
            donnee = self.bdd.hall_of_fame(10)
            y = 0
            for score in donnee:
                self.game.draw_text(f"{score[0]} {score[1]}", 20, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - y)
                y -=20
            

            self.blit_screen()

class PseudoEdit(Menu):
    def __init__(self, game, data):
        Menu.__init__(self, game)
        self.table = data
        if self.table == "Player1":
            self.idx = 0
        elif self.table == "Player2":
            self.idx = 1
        self.state = "valider"
        self.alphabet_List = list(string.ascii_lowercase)
        self.alphabet_Position = []
        self.offset = 50
        self.startx, self.starty = self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 +25
        self.cursor_rect.midtop = (self.startx, self.starty) 
        
        
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Change your pseudo', 40, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 250)
            self.game.draw_text(self.table, 40, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 200)
            self.pseudo = self.bdd.select_data_player(self.table, "Pseudo")
            self.pseudo = list(self.pseudo[0])
            
            self.game.draw_text(self.pseudo[0], 40, self.game.screen_dimension[0] / 2 - 100, self.game.screen_dimension[1] / 2 - 100)
            self.letter0 = [self.game.screen_dimension[0] / 2 - 100, self.game.screen_dimension[1] / 2 - 100 +25]

            self.game.draw_text(self.pseudo[1], 40, self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 100)
            self.letter1 = [self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 - 100 +25]

            self.game.draw_text(self.pseudo[2], 40, self.game.screen_dimension[0] / 2 +100, self.game.screen_dimension[1] / 2 - 100)
            self.letter2 = [self.game.screen_dimension[0] / 2 +100, self.game.screen_dimension[1] / 2 - 100 +25]

            self.game.draw_text("valider", 40,self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2)
            self.button_valider = [self.game.screen_dimension[0] / 2, self.game.screen_dimension[1] / 2 +25]

            self.alphabet_Position = [self.letter0, self.letter1, self.letter2, self.button_valider]
            self.move_cursor()
            self.cursor = self.draw_cursor(0, 0)
            self.blit_screen()
            self.game.reset_keys()


    def check_input(self):
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if round(pygame.joystick.Joystick(self.idx).get_axis(0)) == -1:
                    self.game.LEFT_KEY = True
                if round(pygame.joystick.Joystick(self.idx).get_axis(0)) == 1:
                    self.game.RIGHT_KEY = True
                if round(pygame.joystick.Joystick(self.idx).get_axis(1)) == 1:
                    self.game.DOWN_KEY = True
                if round(pygame.joystick.Joystick(self.idx).get_axis(1)) == -1:
                    self.game.UP_KEY = True
            if event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(self.idx).get_button(0) == 1:
                    self.game.START_KEY = True
                if pygame.joystick.Joystick(self.idx).get_button(1) == 1:
                    self.game.BACK_KEY = True
                    
            if event.type == pygame.QUIT:
                quit()

    def move_cursor(self):
        if self.game.RIGHT_KEY:            
            if self.state == 'letter0':
                self.cursor_rect.midtop = (self.alphabet_Position[1][0], self.alphabet_Position[1][1])
                self.state = 'letter1'
            elif self.state == 'letter1':
                self.cursor_rect.midtop = (self.alphabet_Position[2][0], self.alphabet_Position[2][1])
                self.state = 'letter2'
            elif self.state == 'letter2':
                self.cursor_rect.midtop = (self.alphabet_Position[3][0], self.alphabet_Position[3][1])
                self.state = 'valider'
            elif self.state == 'valider':
                self.cursor_rect.midtop = (self.alphabet_Position[0][0], self.alphabet_Position[0][1])
                self.state = 'letter0'

        if self.game.LEFT_KEY:            
            if self.state == 'letter0':
                self.cursor_rect.midtop = (self.alphabet_Position[3][0], self.alphabet_Position[3][1])
                self.state = 'valider'
            elif self.state == 'letter1':
                self.cursor_rect.midtop = (self.alphabet_Position[0][0], self.alphabet_Position[0][1])
                self.state = 'letter0'
            elif self.state == 'letter2':
                self.cursor_rect.midtop = (self.alphabet_Position[1][0], self.alphabet_Position[1][1])
                self.state = 'letter1'
            elif self.state == 'valider':
                self.cursor_rect.midtop = (self.alphabet_Position[2][0], self.alphabet_Position[2][1])
                self.state = 'letter2'

        if self.game.DOWN_KEY and self.state != "valider":
            if self.state == 'letter0':
                index = self.alphabet_List.index(self.pseudo[0])
                if index == 0:
                    index = 25
                else:
                    index -= 1
                lettre = self.alphabet_List[index]
                self.pseudo[0] = lettre
                self.new_pseudo = lettre + self.pseudo[1] + self.pseudo[2]
                self.bdd.update_name_player(self.table, self.new_pseudo)

            elif self.state == 'letter1':
                index = self.alphabet_List.index(self.pseudo[1])
                if index == 0:
                    index = 25
                else:
                    index -= 1
                lettre = self.alphabet_List[index]
                self.pseudo[1] = lettre
                self.new_pseudo = self.pseudo[0] + lettre + self.pseudo[2]
                self.bdd.update_name_player(self.table, self.new_pseudo)


            elif self.state == 'letter2':
                index = self.alphabet_List.index(self.pseudo[2])
                if index == 0:
                    index = 25
                else:
                    index -= 1
                lettre = self.alphabet_List[index]
                self.pseudo[2] = lettre
                self.new_pseudo = self.pseudo[0] + self.pseudo[1] + lettre
                self.bdd.update_name_player(self.table, self.new_pseudo)
                
        if self.game.UP_KEY and self.state != "valider":
            if self.state == 'letter0':
                index = self.alphabet_List.index(self.pseudo[0])
                if index == 25:
                    index = 0
                else:
                    index += 1
                lettre = self.alphabet_List[index]
                self.pseudo[0] = lettre
                self.new_pseudo = lettre + self.pseudo[1] + self.pseudo[2]
                self.bdd.update_name_player(self.table, self.new_pseudo)

            elif self.state == 'letter1':
                index = self.alphabet_List.index(self.pseudo[1])
                if index == 25:
                    index = 0
                else:
                    index += 1
                lettre = self.alphabet_List[index]
                self.pseudo[1] = lettre
                self.new_pseudo = self.pseudo[0] + lettre + self.pseudo[2]
                self.bdd.update_name_player(self.table, self.new_pseudo)
                
            elif self.state == 'letter2':
                index = self.alphabet_List.index(self.pseudo[2])
                if index == 25:
                    index = 0
                else:
                    index += 1
                lettre = self.alphabet_List[index]
                self.pseudo[2] = lettre
                self.new_pseudo = self.pseudo[0] + self.pseudo[1] + lettre
                self.bdd.update_name_player(self.table, self.new_pseudo)

        if self.game.START_KEY and self.state == 'valider':
            self.game.curr_menu = ConfigGame(self.game)
            self.run_display = False

        if self.game.BACK_KEY:
            self.game.curr_menu = ConfigGame(self.game)
            self.run_display = False










