from bdd import Bdd
import pygame
import math
from game import Game
from pygame.locals import *
from tkinter import *
from tkinter import messagebox


try:
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


    pygame.display.set_caption("Space Versus")
    screen = pygame.display.set_mode((1080,720))

    background = pygame.image.load('assets/Fond-space.png')
    background = pygame.transform.scale(background, (1080,720))


    res = (1080,720)
    game = Game(screen)
    running = True

    while running:

        screen.blit(background, (0,0))
        game.manage_joystick()

        if game.is_playing:
            game.update(screen)
            game.manage_pressed_keys()
        
        else:
            game.curr_menu.display_menu()
            
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                print("Fermeture du jeu")
            elif event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
                if event.key == pygame.K_SPACE:
                    game.player2.shoot()
                if event.key == pygame.K_RCTRL:
                    game.player1.shoot()
            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False
            elif event.type == JOYDEVICEADDED:
                joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
            elif event.type == JOYDEVICEREMOVED:
                joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

except pygame.error as error:
    if str(error) == "video system not initialized":
        print(str(error))
    elif str(error) == "Invalid joystick device number":
        print(str(error))
        Tk().wm_withdraw()
        messagebox.showinfo('Warning','Ce jeu nécessite 2 manettes avec au minimum 1 Joystick et 2 Bouttons pour se lancer.')
        print("Fermeture du jeu")

    