import pygame
from pygame.locals import *

class HealthTable:
    def __init__(self, max = 10):
        self.max = [None] * max

    def __setitem__(self, key, value):
        max_idx = hash(key) % len(self.max)
        self.max[max_idx] = [key, value]

    def __getitem__(self, key):
        max_idx = hash(key) % len(self.max)
        if self.max[max_idx]:
            return self.max[max_idx][1]
        else:
            raise KeyError

    def __contains__(self, key):
        try:
            _ = self[key]
            return True
        except:
            return False

