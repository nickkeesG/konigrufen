import random
import pygame
from game import *
from krypke import *
from view import *

player_names = ['Bruno', 'Jakob', 'Katrin', 'Nadine']

def update_view(game_state, view):
    if view.krypke_mode:
        print("have not yet implemented krypke view")
        init_view(view)
        display_krypke_view(game_state, view)
        if view.dropdown_open:
            display_dropdown(view, game_state.model_list)
    else:
        display_game_view(game_state, view)
    
    pygame.display.update()

def main():

    start_pygame()

    screen = None #this is the screen where everything will be displayed

    cards = init_cards()                #deal the cards to all players
    players = init_players(player_names, cards)
    model_list = init_krypke_models(players)   #initialize the krypke models 
    game_state = Game_State(players, model_list) 

    #the zeroth turn
    call_king(game_state)

    view = View(screen)
    update_view(game_state, view) #first update initializes the view

    game_over = False
    while not game_over:        #GAME LOOP
        for player in players:
            turn_over = False
            dropdown_clicked_already = False
            while not turn_over:
                #if player.contains(Card('heart', 8, 0)):
                #    print(player.name + ":I have it!!!")
                #    player.play(Card('heart', 8, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            nrcards = len(player.hand)-1
                            player.play(player.hand[random.randint(0,nrcards)])
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
                if mouse_pressed:
                    print(pygame.mouse.get_pos())
                    if mouse_over_dropdown(x,y) and not dropdown_clicked_already:
                        dropdown_clicked_already = True
                        view.dropdown_open = not view.dropdown_open
                        update_view(game_state, view)
                    if view.dropdown_open and mouse_over_dropdown_item(x,y,len(game_state.model_list)):
                        view.dropdown_open = False
                        update_view(game_state, view)
                        select_dropdown_item(x,y, game_state.model_list, view)
                else:
                    dropdown_clicked_already = False


                    
                

if __name__ == "__main__":
    main()