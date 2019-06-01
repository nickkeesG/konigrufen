import random
import pygame
from game_environment import *
from krypke import *
from view import *

def update_view(game_state, view):
    if view.krypke_mode:
        print("have not yet implemented krypke view")
        init_view(view)
        display_krypke(view)
        if view.dropdown_open:
            display_dropdown(view, game_state.model_list)
    else:
        display_cards(game_state, view)
    
    pygame.display.update()

def main():

    start_pygame()

    screen = None #this is the screen where everything will be displayed

    cards = init_cards()                #deal the cards to all players
    players = init_players(cards)
    model_list = init_krypke_models()   #initialize the krypke models 
    game_state = Game_State(players, model_list) 

    view = View(screen)
    update_view(game_state, view) #first update initializes the view

    game_over = False
    while not game_over:        #GAME LOOP
        for player in players:
            turn_over = False
            dropdown_clicked_already = False
            while not turn_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            print("turn transitions have not been implemented yet")
                            turn_over = True
                            game_state.krypke_mode = False
                            update_view(game_state, view)
                        if event.key == pygame.K_k :
                            view.krypke_mode = not view.krypke_mode
                            view.dropdown_open = False
                            update_view(game_state, view)
                x, y = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()[0]
                mouse_over_dropdown = is_mouse_over_dropdown(x,y)
                if mouse_pressed and mouse_over_dropdown:
                    if not dropdown_clicked_already:
                        dropdown_clicked_already = True
                        view.dropdown_open = not view.dropdown_open
                        update_view(game_state, view)
                if not mouse_pressed:
                    dropdown_clicked_already = False

                    
                

if __name__ == "__main__":
    main()