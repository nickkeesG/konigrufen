import os
import pygame
import random
from view import *

class Card:
    def __init__(self,suit,value,image,score):
        self.suit = suit
        self.value = value
        self.image = image
        self.score = score

class Game_State:
    def __init__(self, players, model_list, useKnowledge):
        self.players = players
        self.model_list = model_list
        self.king_called = None
        self.called_king_played = False
        self.cards_played = []
        self.recentCard = None
        self.playerTurn = players[0]
        self.maxCardValue = 22
        self.useKnowledge = useKnowledge
        self.nrTrumps = 20
        self.previous_player = None
        self.initMode = True
        self.teamsKnown = False
        self.teamIdx = None
        self.winner = None
        self.winningTeam = []
        self.winningTeamPT = None
        self.noSuitPlayer = None
        self.leading_suit = None

class Knowledge:
    def __init__(self,hasHighestCard,knowsTeammate, trumpAdvantage):
        self.hasHighestCard = hasHighestCard
        self.knowsTeammate = knowsTeammate
        self.trumpAdvantage = trumpAdvantage
        self.opponentLacksSuit = False
        self.lackedSuits = []

class Player:
    def __init__(self, name, hand, knowledge):
        self.name = name
        self.hand = hand
        self.recent_contain = None
        self.played_card = None
        self.teammates = []
        self.teamWonCards = []
        self.finalScore = 0
        self.knowledge = knowledge
        self.alone = False
        self.opponents = []
        self.reason = None

    def contains(self, request):
        for card in self.hand:
            if card.suit == request.suit and card.value == request.value:
                self.recent_contain = card
                return 1
        return 0

    def play(self, card, game_state):
        if self.contains(card):
            self.played_card = self.recent_contain
            print(self.name + " played " + self.played_card.suit + " " + str(self.played_card.value))
            game_state.cards_played.append(self.played_card)
            self.hand.remove(self.played_card)
            if self.played_card.value == game_state.maxCardValue:
                game_state.maxCardValue = determineMaxCard(game_state.players,game_state)
            if self.played_card.suit == game_state.king_called and self.played_card.value == 8:
                game_state.called_king_played = True
            if self.played_card.suit == 'trump':
                game_state.nrTrumps -= 1

    def determineCard(self, leading_suit,game_state, winning_player):
        game_state.noSuitPlayer = None
        game_state.leading_suit = leading_suit
        nrcards = len(self.hand) - 1  # get number of cards

        if self != winning_player: #If not the first player
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
                self.reason = "I will follow the suit"
                return return_card
            elif trump_match: #play trump if you don't have leading suit
                self.reason = "I don't have the suit so I play trump"
                updateNoSuit(self, game_state, leading_suit)
                return return_trump
            else:
                self.reason = "I don't have the suit nor trump so I play a random card"
                updateNoSuit(self,game_state,leading_suit)
                return self.hand[random.randint(0, nrcards)]  # play random card in all other cases
        elif game_state.useKnowledge: #If we want the agents to use knowledge
            if self.knowledge.hasHighestCard: #If you know you have the highest card, play it.
                self.reason = "I know I have the highest card so I play it"
                return getHighestCard(self)
            elif self.knowledge.trumpAdvantage: #If you know you have the majority of trumps, play trumps
                self.reason = "I know I have the majority of trump cards so I play one"
                for trump in self.hand:
                    if trump.suit == 'trump':
                        return trump
            elif self.knowledge.opponentLacksSuit:
                string = ""
                for suit in self.knowledge.lackedSuits:
                    string = string + " " + suit
                self.reason = "I know some of my opponents don't have"+string+" so I play such suits"
                for lackSuit in self.knowledge.lackedSuits:
                    for card in self.hand:
                        if card.suit == lackSuit:
                            return card
        self.reason = "I don't have usable knowledge now, so I play a random card"
        return self.hand[random.randint(0, nrcards)] #play random card in all other cases


def updateNoSuit(player,game_state,leading_suit):
    game_state.noSuitPlayer = player
    game_state.leading_suit = leading_suit
    for p in game_state.players:
        if player in p.opponents:
            p.knowledge.opponentLacksSuit = True
            if leading_suit not in p.knowledge.lackedSuits:
                p.knowledge.lackedSuits.append(leading_suit)

def getHighestCard(player):
    max = -1
    maxCard = None
    for card in player.hand:
        if card.value > max:
            max = card.value
            maxCard = card
    return maxCard

def determineMaxCard(players,game_state):
    max = -1
    for player in players:
        for card in player.hand:
            if (game_state.nrTrumps > 0 and card.suit == 'trump' and card.value > max):
                max = card.value
            elif (game_state.nrTrumps == 0 and card.value > max):
                max = card.value
    return max

def determineWinner(players, leading_suit, game_state):
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
    print(winner.name + " won this round and starts the next one!")
    game_state.winner = winner
    winner.teamWonCards.extend(game_state.cards_played)
    game_state.cards_played = []
    return winner



def determineWinningTeam(players,game_state):
    for player in players:
        ctr = 0
        sum = 0
        idx = 0
        for card in player.teamWonCards:
            sum += card.score
            ctr += 1
            if ctr == 3 or idx == len(player.teamWonCards)-1:
                player.finalScore += (sum + 1)
                print(player.finalScore)
                ctr = 0
                sum = 0
            idx += 1
            #change the 35 limit here because we only play 48 cards, not 54
        if player.finalScore >= 35:
            game_state.winningTeam.append(player)
            game_state.winningTeamPT = player.finalScore
            print(player.name + " won this game with "+str(player.finalScore)+" points")
        else:
            print(player.name + " lost this game with "+str(player.finalScore)+" points")



def determineTeams(players, game_state, caller):
    called_king = game_state.king_called
    if caller.contains(Card(called_king,8,None,4)): #If the caller is playing alone make 1 vs 3 teams
        caller.teammates.append(caller)
        caller.alone = True
        for player in players:
            if player != caller:
                for teammate in players:
                    if teammate != caller:
                        player.teammates.append(teammate)
                        player.teamWonCards = teammate.teamWonCards
    else:
        opponent = None
        for player in players:
            if player != caller:
                if player.contains(Card(called_king,8,None,4)):
                    player.teammates.append(caller)
                    player.teamWonCards = caller.teamWonCards
                    caller.teammates.append(player)
                elif opponent == None:
                    opponent = player
                else:
                    player.teammates.append(opponent)
                    player.teamWonCards = opponent.teamWonCards
                    opponent.teammates.append(player)

    printTeams(players)

    for player in players:
        for p in players:
            if p != player and p not in player.teammates:
                player.opponents.append(p)


def printTeams(players):
    for player in players:
        print(player.name + " is in a team with:")
        for mate in player.teammates:
            print(mate.name)

def printOpponents(players):
    for player in players:
        print(player.name + " is an opponent of:")
        for mate in player.opponents:
            print(mate.name)

def call_king(game_state):
    suits = ['heart', 'diamond', 'spade', 'club']
    random.shuffle(suits)
    game_state.king_called = suits[0]

def updateMaxCardKnowledge(players,game_state):
    max = game_state.maxCardValue
    for player in players:
        player.knowledge.hasHighestCard = False
        for card in player.hand:
            if card.value == max:
                player.knowledge.hasHighestCard = True
                print(player.name + " has the highest card with value:" + str(max))

    updateKripkeMaxCard(players, game_state)

def updateKripkeMaxCard(players, game_state):
    high_card = game_state.model_list[1]

    for i,player in enumerate(players):
        high_card.relations[i] = []
        high_card.worlds[i].true_world = player.knowledge.hasHighestCard
        if player.knowledge.hasHighestCard:
            exclude = i
            high_card.relations[i].append((i, i))

    for i in range(0,4):
        for j in range(0,4):
            for k in range(j,4):
                if i != exclude and j != i and i != k:
                    high_card.relations[i].append((j, k))


def updateTeammateKnowledge(players,game_state):
    if not game_state.called_king_played:
        called_king = game_state.king_called
        for player in players:
            if player.contains(Card(called_king,8,None,4)):
                player.knowledge.knowsTeammate = True

                if player.teammates[0].name != player.name:
                    print(player.name + " knows (s)he's in a team with")
                    for mate in player.teammates:
                        print(mate.name)
                else:
                    print(player.name + " knows (s)he's playing alone")
    else:
        for player in players:
            player.knowledge.knowsTeammate = True
            game_state.teamsKnown = True
            print("TEAMS ARE COMMONG KNOWLEDGE KNOW MAYBE ADD THIS TO VIEW")
    updateKripkeTeams(players,game_state)

def updateKripkeTeams(players,game_state):
    teams = game_state.model_list[0]

    if game_state.initMode:
        #set true world process
        for player in players:
            if player.knowledge.knowsTeammate:
                teamWorlds = teams.worlds
                if len(player.teammates) == 1 and player.teammates[0] != player:
                    trueTeam = player.teammates.copy()
                    trueTeam.append(player)
                    for i,tw in enumerate(teamWorlds):
                        if(len(tw.team1) == 2):
                            if (tw.team1[0] == trueTeam[0].name and tw.team1[1] == trueTeam[1].name) or (
                                    tw.team1[1] == trueTeam[0].name and tw.team1[0] == trueTeam[1].name) or (
                                    tw.team2[0] == trueTeam[0].name and tw.team2[1] == trueTeam[1].name) or (
                                    tw.team2[1] == trueTeam[0].name and tw.team2[0] == trueTeam[1].name):
                                tw.true_world = True
                                trueIdx = i
                                game_state.teamIdx = i
                else:
                    for i,tw in enumerate(teamWorlds):
                        if (len(tw.team1) == 1 and tw.team1[0] == player.name) or (len(tw.team2)==1 and tw.team2[0] == player.name):
                            tw.true_world = True
                            trueIdx = i
                            game_state.teamIdx = i
                break
        game_state.initMode = False
    if not game_state.teamsKnown:
        for i, p in enumerate(players):
            if p.knowledge.knowsTeammate:
                exclude = i

                teams.relations[i].append((game_state.teamIdx, game_state.teamIdx))

        for i in range(0, 4):
            for j in range(0, 4):
                for k in range(j, 4):
                    if i != exclude and j != i and i != k:
                        teams.relations[i].append((j, k))
    else:
        for i, p in enumerate(players):
            teams.relations[i] = []
            teams.relations[i].append((game_state.teamIdx, game_state.teamIdx))




def updateTrumpKnowledge(players,game_state):
    for player in players:
        trumpCtr = 0
        for card in player.hand:
            if card.suit == 'trump':
                trumpCtr += 1
        print(player.name + " has " + str(trumpCtr) + " trumps, the total nr is " + str(game_state.nrTrumps))
        if trumpCtr > (game_state.nrTrumps/2):
            player.knowledge.trumpAdvantage = True

def updateKnowledge(players, game_state):
    updateMaxCardKnowledge(players, game_state)
    updateTeammateKnowledge(players, game_state)
    updateTrumpKnowledge(players, game_state)

def checkIfLastPlay(players):
    for player in players:
        if player.hand != []:
            return False
    return True
def executePlay(player, winning_player, played_card_counter, leading_suit, players, endOfRound, game_state):
    card_to_be_played = player.determineCard(leading_suit,game_state,winning_player) #pick random card
    game_state.recentCard = card_to_be_played
    if player == winning_player:  # Reset winning player variable and set leading suit
        leading_suit = card_to_be_played.suit
        winning_player = None
    player.play(card_to_be_played, game_state)
    if not checkIfLastPlay(players):
        updateKnowledge(players,game_state)

    played_card_counter += 1

    print("won cards: " + str(len(player.teamWonCards)))
    if played_card_counter == 4: #check if all players put a card, if so determine the winner of the round
        winning_player = determineWinner(players, leading_suit, game_state)
        played_card_counter = 0
        endOfRound = True

        if not winning_player.hand:  # if the last card is played, determine winning team
            determineWinningTeam(players,game_state)
    return winning_player, played_card_counter, leading_suit, endOfRound, game_state

def init_cards():
    #Note, we left out the first card of each suit, and the 2nd and 3rd trump card in order to be sure the most important cards are
    #contained in the game. We don't include the part of the game where one player initially chooses to swap 1,2 or 3 cards etc.
    cards = []
    #trump cards are simplified to 1-22 (the joker is counted as 22)
    img = load_image('joker.png')
    cards.append(Card('trump',22,img,4))
    for i in range(1, 22):
        if i == 1 or i == 21:
            score = 4
        else:
            score = 0
        if i == 2 or i==3:
            continue
        else:
            img = load_image('trump'+str(i)+'.png')
            cards.append(Card('trump', i, img, score))

    suits = ['heart', 'diamond', 'spade', 'club']
    for s in suits: #suit cards are simplified to 1-8, where 8 is the king
        img = load_image(s + '_k.png')      #king
        cards.append(Card(s, 8, img,4))
        img = load_image(s + '_q.png')      #Queen
        cards.append(Card(s, 7, img,3))
        img = load_image(s + '_c.png')      #Cavalier
        cards.append(Card(s, 6, img,2))
        img = load_image(s + '_j.png')      #Jack
        cards.append(Card(s, 5, img,1))

        number_cards = ['_7', '_8', '_9', '_10']
        if s == 'heart' or s == 'diamond': #red numbers go in the opposite direction
            number_cards = ['_4', '_3', '_2', '_1']
        
        for i in range(2,5):
            img = load_image(s + number_cards[i-1] + '.png')
            cards.append(Card(s, i, img,0))
    print(len(cards))
    random.shuffle(cards)
    return cards

def init_players(player_names, cards):
    players = []
    highest = False
    for name in player_names:
        hand = []
        for i in range(0,12):
            c = cards.pop()
            hand.append(c)
            if c.suit == 'trump' and c.value == 22:
                highest = True
        p = Player(name, hand, Knowledge(highest,False,False))
        highest=False
        players.append(p)
    return players