import os
import random
import pygame
from krypke import *

screen_size = (1050, 650)
board_size = (800, 800)
card_size = (45, 90)

FONT = 'ubuntu'
dropdown = pygame.Rect(30, 50, 200, 20)

class View:
    def __init__(self, screen):
        self.screen = screen
        self.krypke_mode = False
        self.dropdown_open = False

def blit_card(card, location, orientation, view):
    img = card.image
    img = pygame.transform.scale(img, card_size)
    img = pygame.transform.rotate(img, orientation)
    if orientation == 0 or orientation == 180:
        location = (location[0] - card_size[0]/2, location[1] - card_size[1]/2)
    if orientation == 90 or orientation == 270:
        location = (location[0] - card_size[1]/2, location[1] - card_size[0]/2)
    view.screen.blit(img, location)

def display_cards(game_state, view):
    init_view(view)

    #these are the positions of the first cards displayed
    positions = [(screen_size[0] - board_size[0] + 150,50), (screen_size[0] - 50, 100), (screen_size[0] - 150, screen_size[1] -50), (screen_size[0] - board_size[0] + 50, screen_size[1] - 100)]

    #offset between one card and the next
    directions = [(card_size[0] +1,0), (0, card_size[0] +1), (-card_size[0] -1, 0), (0, -card_size[0] -1)]

    for i in range(0,4):
        player = game_state.players[i]
        position = positions[i]
        d = directions[i]
        for c in player.hand:
            blit_card(c, position, i*90, view)
            position = (position[0]+d[0], position[1]+d[1])

def display_dropdown(view, model_list):
    dropdown_font = pygame.font.SysFont(FONT, 16)

    item_height = 20
    item_position = dropdown.top + dropdown.height

    for m in model_list:
        item = pygame.Rect(dropdown.left, item_position, dropdown.width, item_height)
        pygame.draw.rect(view.screen, (0, 0, 0), item, 1)
        item_message = dropdown_font.render(m.name, 1, (0, 0, 0))
        view.screen.blit(item_message, ((item.left + 5), item.top))
        item_position += item_height


def display_krypke(view):
    dropdown_font = pygame.font.SysFont(FONT, 16)
    pygame.draw.rect(view.screen, (0, 0, 0), dropdown, 1)
    dropdown_message = dropdown_font.render('choose a krypke model', 1, (0, 0, 0))
    view.screen.blit(dropdown_message, ((dropdown.left + 5), dropdown.top))

def init_view(view):
    view.screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
    view.screen.fill((100, 100, 100), pygame.Rect(0, 0, screen_size[0], screen_size[1]))
    view.screen.fill((255, 255, 255), pygame.Rect(0, 0, screen_size[0] - board_size[0], screen_size[1]))

def is_mouse_over_dropdown(x, y):
    if x < dropdown.left or x > dropdown.left + dropdown.width:
        return False
    if y < dropdown.top or y > dropdown.top + dropdown.height:
        return False
    return True

def load_image(name):
    fullname = os.path.join('img', name)
    try:
        image=pygame.image.load(fullname)
        return image
    except pygame.error:
        print('Cannot load image: ' +  str(name))
        raise SystemExit

def start_pygame():
    pygame.init()           #start pygame :)
    pygame.font.init()