import random
import pygame

class World:
    def __init__(self, name):
        self.name = name
        self.true_world = False

class Krypke_Model:
    def __init__(self, name, players):
        self.name = name
        self.agents = [p.name for p in players]
        self.worlds = []
        self.relations = []

def init_krypke_models(players):
    model_list = []
    model_list.append(Krypke_Model("model1", players))

    high_card = Krypke_Model("Who has the highest card?", players)
    high_card.worlds = [World(p.name) for p in players]
    model_list.append(high_card)

    model_list.append(Krypke_Model("model3", players))
    return model_list

