import os
import random
import pygame
from krypke import *

screen_size = (1050, 650)
board_size = (800, 650)
card_size = (45, 90)

pi = 3.14159

FONT = 'ubuntu'
dropdown = pygame.Rect(30, 50, 200, 20)
dropdown_item_height = 20

agent_colors = [(255, 0, 0), (127, 255, 0), (0, 255, 255), (127, 0, 255)]
world_positions = [(-160,-160), (160,-160), (-160,160), (160,160), (0,-240), (0,240), (-240,0), (240,0)]

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
    #these are the positions of the first cards displayed
    positions = [(screen_size[0] - board_size[0] + 150,70), (screen_size[0] - 70, 100), (screen_size[0] - 150, screen_size[1] -70), (screen_size[0] - board_size[0] + 70, screen_size[1] - 100)]

    #offset between one card and the next
    directions = [(card_size[0] +1,0), (0, card_size[0] +1), (-card_size[0] -1, 0), (0, -card_size[0] -1)]

    name_font = pygame.font.SysFont(FONT, 16)
    for i in range(0,4):
        player = game_state.players[i]
        position = positions[i]
        d = directions[i]
        for c in player.hand:
            blit_card(c, position, i*90, view)
            position = (position[0]+d[0], position[1]+d[1])

        #print the name
        name_message = name_font.render(player.name, 1, agent_colors[i])
        location = (0, 0)
        orientation = 0
        if i == 0:
            location = (positions[i][0], 0)
        elif i == 1:
            location = (screen_size[0]-20, positions[i][1])
            orientation = 90
        elif i == 2:
            location = (positions[i][0]-50,screen_size[1]-20)
        elif i == 3:
            location = (screen_size[0]-board_size[0], positions[i][1]-50)
            orientation = 270
        name_message = pygame.transform.rotate(name_message, orientation)
        view.screen.blit(name_message, location)

def display_dropdown(view, model_list):
    dropdown_font = pygame.font.SysFont(FONT, 16)

    item_position = dropdown.top + dropdown.height

    for m in model_list:
        item = pygame.Rect(dropdown.left, item_position, dropdown.width, dropdown_item_height)
        pygame.draw.rect(view.screen, (0, 0, 0), item, 1)
        item_message = dropdown_font.render(m.name, 1, (0, 0, 0))
        view.screen.blit(item_message, ((item.left + 5), item.top))
        item_position += dropdown_item_height

def display_game_view(game_state, view):
    init_view(view)
    display_cards(game_state, view)
    display_sidebar(game_state, view)

def display_krypke_view(game_state, view):

    #display dropdown select
    dropdown_font = pygame.font.SysFont(FONT, 16)
    pygame.draw.rect(view.screen, (0, 0, 0), dropdown, 1)
    dropdown_message = dropdown_font.render('choose a krypke model', 1, (0, 0, 0))
    view.screen.blit(dropdown_message, ((dropdown.left + 5), dropdown.top))

    sidebar_font = pygame.font.SysFont(FONT, 16)

    #legend
    agents_title = sidebar_font.render('agents:', 1, (0, 0, 0))
    view.screen.blit(agents_title, (35, 200))
    position = (55, 220)
    for i in range(0, len(game_state.players)):
        agent_message = sidebar_font.render(game_state.players[i].name, 1, agent_colors[i])
        view.screen.blit(agent_message, position)
        position = (55, position[1]+20)
    view.screen.fill((100, 100, 100), pygame.Rect(35, 350, 82, 20))
    true_world_message = sidebar_font.render('True World', 1, (255, 255, 0))
    view.screen.blit(true_world_message, (35, 350))

def display_model(model, view):
    model_font = pygame.font.SysFont(FONT, 16)
    model_title = model_font.render(model.name, 1, (0, 0, 0))
    view.screen.blit(model_title, ((screen_size[0] - board_size[0]/2 - 300), 20))

    #display the worlds
    center = (screen_size[0] - board_size[0]/2, board_size[1]/2)
    for i in range(0,len(model.worlds)):
        model.worlds[i].position = (world_positions[i][0]+center[0], world_positions[i][1]+center[1])
        world_color = (0, 0, 0)
        if model.worlds[i].true_world:
            world_color = (255, 255, 0)
        world_name = model_font.render(model.worlds[i].name, 1, world_color)
        view.screen.blit(world_name, (model.worlds[i].position))

    #display the relations
    offset = 10
    for i in range(0, len(model.agents)):
        relations = model.relations[i]
        for r in relations:
            (s, e) = r
            
            if not s == e: #the non-reflexive case
                start_pos = model.worlds[s].position
                end_pos = model.worlds[e].position

                #format line location to look better
                average = (start_pos[0]*0.5 + end_pos[0]*0.5 + 80, start_pos[1]*0.5 + end_pos[1]*0.5 + 20)
                start_pos = (start_pos[0]*0.8 + average[0]*0.2, start_pos[1]*0.8 + average[1]*0.2)
                end_pos = (end_pos[0]*0.8 + average[0]*0.2, end_pos[1]*0.8 + average[1]*0.2)

                #apply the offset
                diff = (start_pos[0]-end_pos[0], start_pos[1]-end_pos[1])
                direction = (diff[1]*abs(diff[1])/(abs(diff[0]*diff[0])+abs(diff[1]*diff[1])), diff[0]*abs(diff[0])/(abs(diff[0]*diff[0])+abs(diff[1]*diff[1])))
                direction = (-direction[0]*((len(model.agents)/2)- i)*offset, direction[1]*((len(model.agents)/2)- i)*offset)
                start_pos = (start_pos[0]+direction[0], start_pos[1]+direction[1])
                end_pos = (end_pos[0]+direction[0], end_pos[1]+direction[1])

                pygame.draw.line(view.screen, agent_colors[i], start_pos , end_pos, 2)
            else: #the reflexive case
                size = i*offset
                pygame.draw.arc(view.screen, agent_colors[i], ((model.worlds[s].position[0]-size-20, model.worlds[s].position[1]-size-20), (30+size, 30+size)),0*pi, 1.5*pi)


    pygame.display.update() #update view will not be called, so we must update the display here

def display_sidebar(game_state, view):
    sidebar_font = pygame.font.SysFont(FONT, 16)
    instruction_a = sidebar_font.render('press k for krypke view', 1, (0, 0, 0))
    instruction_b = sidebar_font.render('press space for next turn', 1, (0, 0, 0))
    view.screen.blit(instruction_a, (10,10))
    view.screen.blit(instruction_b, (10,30))

    king_called_message_a = sidebar_font.render(str(game_state.players[0].name) + ' is playing and has called', 1, (0, 0, 0))
    king_called_message_b = sidebar_font.render(' for the king of ' + game_state.king_called + 's', 1, (0, 0, 0))
    view.screen.blit(king_called_message_a, (10, 70))
    view.screen.blit(king_called_message_b, (10, 90))

def init_view(view):
    view.screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
    view.screen.fill((100, 100, 100), pygame.Rect(0, 0, screen_size[0], screen_size[1]))
    view.screen.fill((255, 255, 255), pygame.Rect(0, 0, screen_size[0] - board_size[0], screen_size[1]))

def load_image(name):
    fullname = os.path.join('img', name)
    try:
        image=pygame.image.load(fullname)
        return image
    except pygame.error:
        print('Cannot load image: ' +  str(name))
        raise SystemExit

def mouse_over_dropdown(x, y):
    if x < dropdown.left or x > dropdown.left + dropdown.width:
        return False
    if y < dropdown.top or y > dropdown.top + dropdown.height:
        return False
    return True

def mouse_over_dropdown_item(x, y, length):
    if x < dropdown.left or x > dropdown.left + dropdown.width:
        return False
    if y < dropdown.top + dropdown.height or y > dropdown.top + dropdown.height + dropdown_item_height*length:
        return False
    return True

def select_dropdown_item(x, y, model_list, view):
    item_offset = 0
    for m in model_list:
        if y > dropdown.top + dropdown.height + item_offset and y < dropdown.top + dropdown.height + item_offset + dropdown_item_height:
            display_model(m, view)
        item_offset = item_offset + dropdown_item_height

def start_pygame():
    pygame.init()           #start pygame :)
    pygame.font.init()