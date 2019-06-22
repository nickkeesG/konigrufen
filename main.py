import random
import pygame
from game import *
from krypke import *
from view import *
from game import *
import time
player_names = ['Bruno', 'Jakob', 'Katrin', 'Nadine']
useKnowledge = True
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

def startGame():

    start_pygame()

    screen = None #this is the screen where everything will be displayed

    cards = init_cards()                #deal the cards to all players
    players = init_players(player_names, cards)
    model_list = init_krypke_models(players)   #initialize the krypke models
    game_state = Game_State(players, model_list, useKnowledge)

    #the zeroth turn
    call_king(game_state)
    determineTeams(players, game_state, players[0])
    updateKnowledge(players,game_state)
    view = View(screen)
    update_view(game_state, view) #first update initializes the view
    game_over = False
    winning_player = players[0]
    played_card_counter = 0
    leading_suit = None
    endOfRound = False
    kripkeOn = False
    previous_player = players[0]
    while not game_over:        #GAME LOOP
        for player in players:
            turn_over = False
            dropdown_clicked_already = False
            while not turn_over:
                if winning_player != None and player != winning_player: #Make sure the winning player gets to start
                    break

                if not kripkeOn:
                    game_state.playerTurn = previous_player
                    #update_view(game_state, view)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            winning_player, played_card_counter, leading_suit, endOfRound, game_state = executePlay(player, winning_player, played_card_counter, leading_suit, players, endOfRound, game_state)
                            turn_over = True
                            game_state.krypke_mode = False

                            game_state.previous_player = player
                            update_view(game_state, view)

                            if endOfRound:
                                #time.sleep(2)
                                leading_suit = None
                                for player in players:
                                    player.played_card = None
                                    endOfRound = False
                                    game_state.winner = None

                        if event.key == pygame.K_k :
                            if kripkeOn:
                                kripkeOn=False
                            else:
                                kripkeOn = True
                            view.krypke_mode = not view.krypke_mode
                            view.dropdown_open = False
                            update_view(game_state, view)
                        if event.key == pygame.K_n:
                            pygame.display.quit()
                            pygame.quit()
                            startGame()

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
                previous_player = player

def main():
    startGame()

if __name__ == "__main__":
    main()