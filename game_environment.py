import os
import pygame
import random

screen_size = (1050, 650)
board_size = (800, 800)
card_size = (45, 90)
FONT = 'ubuntu'

class Card:
    def __init__(self,suit,value,image):
        self.suit = suit
        self.value = value
        self.image = image

class Game_State:
    def __init__(self, players):
        self.players = players
        self.krypke_mode = False

class Player:
    def __init__(self, name, hand):
      self.name = name
      self.hand = hand

def blit_card(card, location, orientation, screen):
    img = card.image
    img = pygame.transform.scale(img, card_size)
    img = pygame.transform.rotate(img, orientation)
    if orientation == 0 or orientation == 180:
        location = (location[0] - card_size[0]/2, location[1] - card_size[1]/2)
    if orientation == 90 or orientation == 270:
        location = (location[0] - card_size[1]/2, location[1] - card_size[0]/2)
    screen.blit(img, location)
    return screen

def display_cards(game_state, screen):
    screen = init_screen(screen)

    #these are the positions of the first cards displayed
    positions = [(screen_size[0] - board_size[0] + 150,50), (screen_size[0] - 50, 100), (screen_size[0] - 150, screen_size[1] -50), (screen_size[0] - board_size[0] + 50, screen_size[1] - 100)]

    #offset between one card and the next
    directions = [(card_size[0] +1,0), (0, card_size[0] +1), (-card_size[0] -1, 0), (0, -card_size[0] -1)]

    for i in range(0,4):
        player = game_state.players[i]
        position = positions[i]
        d = directions[i]
        for c in player.hand:
            screen = blit_card(c, position, i*90, screen)
            position = (position[0]+d[0], position[1]+d[1])

    pygame.display.update()
    return screen

def init_cards():
    cards = []
    #trump cards are simplified to 1-22 (the joker is counted as 22)
    img = load_image('joker.png')
    cards.append(Card('trump',22,img))
    for i in range(1, 22): 
        img = load_image('trump'+str(i)+'.png')
        cards.append(Card('trump', i, img))

    suits = ['heart', 'diamond', 'spade', 'club']
    for s in suits: #suit cards are simplified to 1-8, where 8 is the king
        img = load_image(s + '_k.png')      #king
        cards.append(Card(s, 8, img))
        img = load_image(s + '_q.png')      #Queen
        cards.append(Card(s, 7, img))
        img = load_image(s + '_c.png')      #Cavalier
        cards.append(Card(s, 6, img))
        img = load_image(s + '_j.png')      #Jack
        cards.append(Card(s, 5, img))

        number_cards = ['_7', '_8', '_9', '_10']
        if s == 'heart' or s == 'diamond': #red numbers go in the opposite direction
            number_cards = ['_4', '_3', '_2', '_1']
        
        for i in range(1,5):
            img = load_image(s + number_cards[i-1] + '.png')
            cards.append(Card(s, i, img))    

    random.shuffle(cards)
    return cards

def init_players(cards):
    player_names = ['Bruno', 'Jakob', 'Katrin', 'Nadine']
    players = []
    for name in player_names:
        hand = []
        for i in range(0,12):
            c = cards.pop()
            hand.append(c)
        p = Player(name, hand)
        players.append(p)
    return players

def init_screen(screen):
    pygame.init()
    pygame.font.init()
    name_font = pygame.font.SysFont(FONT, 20)
    message_font = pygame.font.SysFont(FONT, 16)
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
    screen.fill((100, 100, 100), pygame.Rect(0, 0, screen_size[0], screen_size[1]))
    screen.fill((255, 255, 255), pygame.Rect(0, 0, screen_size[0] - board_size[0], screen_size[1]))
    pygame.display.update()

    return screen

def load_image(name):
    fullname = os.path.join('img', name)
    try:
        image=pygame.image.load(fullname)
        return image
    except pygame.error:
        print('Cannot load image: ' +  str(name))
        raise SystemExit