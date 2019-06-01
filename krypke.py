import random
import pygame

class Krypke_Model:
    def __init__(self, name):
        self.name = name

def init_krypke_models():
    model_list = []
    model_list.append(Krypke_Model("Who's on my team?"))
    model_list.append(Krypke_Model("Who has the highest card?"))
    model_list.append(Krypke_Model("model3"))
    return model_list

