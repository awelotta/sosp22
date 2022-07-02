from operator import add
from enum import Enum, auto
from iteration_utilities import duplicates

class Game: # interface for shared state between clients, e.g. positions... that should suffice for mvp
    def __init__(self):
        self.size = (15, 15)
        self.ppos = [[0,0], list( map(add, self.size, (-1, -1)) )]
    def move_collide(self, p, direction):
        """returns collisions"""
        self.ppos[p] = list( map(add, self.ppos[p], direction) )
        collisions = list(duplicates(self.ppos)) #idk 
        return collisions
