import random
import pygame

class World:
    def __init__(self, name):
        self.name = name
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
    model_list.append(Krypke_Model("model1", players))

    high_card = Krypke_Model("Who has the highest card?", players)
    high_card.worlds = [World(p.name) for p in players]
    high_card.worlds[0].true_world = True
    high_card.relations[0].append((0, 0))
    for i in range(1,4):
        for j in range(0,4):
            for k in range(j,4):
                high_card.relations[i].append((j, k))
    model_list.append(high_card)

    model_list.append(Krypke_Model("model3", players))
    return model_list

