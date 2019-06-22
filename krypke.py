import random
import pygame

class playerWorld:
    def __init__(self, player):
        self.name = player.name
        self.true_world = player.knowledge.hasHighestCard
        self.position = None

class teamWorld:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.true_world = False
        self.position = None


class Krypke_Model:
    def __init__(self, name, players):
        self.name = name
        self.agents = [p.name for p in players]
        self.worlds = []
        self.relations = [[] for a in self.agents]


def init_krypke_models(players):
    model_list = []
    model_list.append(init_teamknowledge(players))
    model_list.append(init_highest_card(players))
    return model_list

def init_highest_card(players):
    high_card = Krypke_Model("Who has the highest card?", players)
    high_card.worlds = [playerWorld(p) for p in players]
    for i, p in enumerate(players):
        if p.knowledge.hasHighestCard:
            exclude = i
            high_card.relations[i].append((i, i))
    for i in range(0, 4):
        for j in range(0, 4):
            for k in range(j, 4):
                if i != exclude and j != i and i != k:
                    high_card.relations[i].append((j, k))
    return high_card

def init_teamknowledge(players):
    names = [p.name for p in players]
    teams = Krypke_Model("What are the teams?", players)
    #1 vs 3 teams
    team1 = []
    team1.append(names[0])
    team2 = []
    team2.append(names[1])
    team2.append(names[2])
    team2.append(names[3])
    teams.worlds.append(teamWorld(team1,team2))
    # for i in range (0,4):
    #     team1 = []
    #     team1.append(names[i])
    #     team2 = []
    #     for j in range(0,4):
    #         if j!=i:
    #             team2.append(names[j])
    #
    #     teams.worlds.append(teamWorld(team1,team2))

    #2 vs 2 teams
    for i in range(1, 4):
        team1 = []
        team1.append(names[0])
        team1.append(names[i])
        team2 = []
        for j in range(1, 4):
            if j != i:
                team2.append(names[j])
        teams.worlds.append(teamWorld(team1, team2))



    return teams