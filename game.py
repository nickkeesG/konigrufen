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
        self.king_called = ''



class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
        self.recent_contain = None
        self.played_card = None

    def contains(self, request):
        for card in self.hand:
            if card.suit == request.suit and card.value == request.value:
                self.recent_contain = card
                return 1
        return 0

    def play(self, card):
        if self.contains(card):
            self.played_card = self.recent_contain
            print(self.name + " played " + self.played_card.suit + " " + str(self.played_card.value))
            self.hand.remove(self.played_card)

    def determineCard(self, leading_suit):
        nrcards = len(self.hand) - 1  # get number of cards
        if leading_suit != None: #If not the first player
            return_card = None
            return_trump = None
            suit_match = False
            trump_match = False
            for card in self.hand:
                if card.suit == leading_suit:
                    suit_match = True
                    return_card = card
                elif card.suit == 'trump':
                    trump_match = True
                    return_trump = card

            if suit_match: #play suit if you posess leading suit
                return return_card
            elif trump_match: #play trump if you don't have leading suit
                return return_trump
        return self.hand[random.randint(0, nrcards)] #play random card if you don't have either



def determineWinner(players, leading_suit):
    max = -1
    trumpMax = -1
    winner = None
    trumpInPlay = False
    for player in players:
        value = player.played_card.value
        suit = player.played_card.suit
        if suit == 'trump' and leading_suit != 'trump':
            trumpInPlay = True
        if (not trumpInPlay and suit == leading_suit and value > max) or (trumpInPlay and suit == 'trump' and value > trumpMax):
            if trumpInPlay:
                trumpMax = value
                winner = player
            else:
                max = value
                winner = player
    print(winner.name + " won this round!")
    return winner

def call_king(game_state):
    suits = ['heart', 'diamond', 'spade', 'club']
    random.shuffle(suits)
    game_state.king_called = suits[0]

def executePlay(player, winning_player, played_card_counter, leading_suit, players, endOfRound):
    card_to_be_played = player.determineCard(leading_suit) #pick random card
    if player == winning_player:  # Reset winning player variable and set leading suit
        leading_suit = card_to_be_played.suit
        winning_player = None
    player.play(card_to_be_played)
    played_card_counter += 1
    if played_card_counter == 4: #check if all players put a card, if so determine the winner of the round
        winning_player = determineWinner(players, leading_suit)
        played_card_counter = 0
        endOfRound = True
    return winning_player, played_card_counter, leading_suit, endOfRound

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

def init_players(player_names, cards):
    players = []
    for name in player_names:
        hand = []
        for i in range(0,12):
            c = cards.pop()
            hand.append(c)
        p = Player(name, hand)
        players.append(p)
    return players