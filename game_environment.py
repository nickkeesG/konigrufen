import os
import pygame
import random
from view import *

class Card:
    def __init__(self,suit,value,image):
        self.suit = suit
        self.value = value
        self.image = image

class Game_State:
    def __init__(self, players, model_list):
        self.players = players
        self.model_list = model_list

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

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