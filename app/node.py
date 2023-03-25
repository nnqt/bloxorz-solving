#  Copyright (c) 2020. Abhilshit Soni
import json

from app.block import Block
from app.move import Move
from app.terrain import Terrain


class Node:
    """
    An A* Node object. Wraps the Block object along with f, g, h values at the node. Maintains reference of parent node
    """
    def __init__(self, block: Block, move: Move, parent, terrain: Terrain, f=0, g=0, h=0, reward = 0, n = 0, q=0 ):
        # placeholders for A* costs only to be used in A* solver
        self.f = f
        self.g = g
        self.h = h
        # MCTS reward point
        self.reward = reward
        self.n = n
        self.q = q
        # 
        self.block = block
        self.move = move
        self.parent = parent
        self.terrain = terrain

    def __str__(self):
        json.dumps([str(self.block), str(self.move), str(self.parent), str(self.f), str(self.g), str(self.h)])

    def __eq__(self, __o: object) -> bool:
        if self.block == __o.block and self.terrain == __o.terrain:
            return True
        else:
            return False