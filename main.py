import random
import pygame
from game_environment import *

def update_view(game_state, screen):
    if game_state.krypke_mode:
        print("have not yet implemented krypke view")
        screen = init_screen(screen)
    else:
        screen = display_cards(game_state, screen)
    return screen

def main():
    screen = None #this is the screen where everything will be displayed
    screen = init_screen(screen)

    cards = init_cards()
    players = init_players(cards)
    game_state = Game_State(players)

    game_over = False
    while not game_over:
        for player in players:
            turn_over = False
            while not turn_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            print("turn transitions have not been implemented yet")
                            turn_over = True
                            game_state.krypke_mode = False
                            screen = update_view(game_state, screen)
                        if event.key == pygame.K_k :
                            game_state.krypke_mode = not game_state.krypke_mode
                            screen = update_view(game_state, screen)
                

if __name__ == "__main__":
    main()