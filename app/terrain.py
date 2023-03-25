#  Copyright (c) 2020. Abhilshit Soni

from app.position import Position
from app.block import Block
from app.move import Move
import json
import copy


class Terrain:
    """
    Class Terrain represents the terrain of the game. Terrain contains a
        1. map of traversable and non-traversable areas, represented by True and False boolean values
        2. A start location representing initial location of the bloxorz block (in standing position at start)
        3. A goal location representing the target/ goal to be reached inorder to solve the game
        4. width representing the total columns of the terrain of level-1 bloxorz
        5. height representing the total rows of the terrain of level-1 bloxorz
    """
    map = None  # boolean map of traversable and non-traversable areas
    start = None # start location of the bloxorz block
    goal = None # goal location of the bloxorz block to be reached in order to solve the game level-1
    switchX = None
    bridge_switchX = []
    switchO = None
    bridge_switchO = []
    switchE = None
    switchF = None
    switchG = None
    bridge_with_multi_switch = []
    height = 0
    width = 0
    half_boards = []

    def __init__(self, level_file="resources/level01.txt"):
        """
        initializes Terrain object by parsing the level file provided as an input.
        :param level_file: level file representing the bloxorz level 1 positions
        """
        self.parse_terrain(level_file)

    def can_hold(self, b: Block) -> bool:
        """
        Returns true if Terrain can hold the block completely. As in, both the cubes of bloxorz block should be at the
        legal locations on the terrain map represented by boolean True values in the map.
        :param b: Block object to be verified if it is occupying legal/allowed positions.
        :return: True if Terrain can hold the block completely, else return False
        """
        try:
            flag = False
            if b.p1.x < 0 or b.p1.y < 0 or b.p2.x < 0 or b.p2.y < 0 :
                flag = True
            if b.p1.x > self.height or b.p1.y >self.width or b.p2.x >self.height or b.p2.y >self.width:
                flag = True
            if b.is_standing() and (b.p1 in self.half_boards):
                flag = True
            can_hold = self.map[b.p1.x][b.p1.y] and self.map[b.p2.x][b.p2.y] and not flag
        except IndexError:
            can_hold = False  # print("Warning: "+ str(b.p1) + " or " + str(b.p2) + " is out of range !!")

        return can_hold

    def neighbours(self, b: Block) -> list:
        """
        Gets the neighbours (potential block positions) based on the allowed moves (up,down,left,right)
         from the current position of the block
        :param b: Block object whose neighbours are to be returned
        :return: list of (Block, Move) Tuple representing neighbouring blocks and move required to reach their
        respective block positions
        """
        return [(b.up(), Move.Up), (b.down(), Move.Down), (b.left(), Move.Left), (b.right(), Move.Right)]

    def legal_neighbors(self, b: Block) -> list:
        """
        Filters the list of neighbours by checking if the neighbours are on legally allowed postions on the terrain map
        :param b: Block object whose legal neighbours are to be returned
        :return: list of (Block, Move) Tuple representing legally allowed neighbouring blocks and move required to reach
         their respective block positions
        """
        legal_neighbors = []
        for (n, move) in self.neighbours(b):
            temp_terrain = copy.deepcopy(self)
            if(self.can_hold(n)):
                if self.is_press_switchX(n):
                    for point in self.bridge_switchX:
                        temp_terrain.map[point.x][point.y] = not self.map[point.x][point.y]
                if self.is_press_switchF(n):
                    for point in self.bridge_with_multi_switch:
                        temp_terrain.map[point.x][point.y] = False
                if self.is_press_switchE(n):
                    for point in self.bridge_with_multi_switch:
                        temp_terrain.map[point.x][point.y] = not self.map[point.x][point.y]
                if self.is_press_switchG(n):
                    for point in self.bridge_with_multi_switch:
                        temp_terrain.map[point.x][point.y] = True
                if self.is_press_switchO(n):
                    for point in self.bridge_switchO:
                        temp_terrain.map[point.x][point.y] = not self.map[point.x][point.y]
                legal_neighbors.append((n, move, temp_terrain))    
        return legal_neighbors
        #return [(n, move, self) for (n, move) in self.neighbours if self.can_hold(n)]

    def done(self, b: Block) -> bool:
        """
        Returns true if the current block is at the goal position. The goal is reached only if the Block is in standing
        position and if the position of the block is equal to position of the goal.
        :param b: Block object to be verified whether it has reached the goal
        :return: True if block has reached the goal and is in a standing postion,  else return False
        """
        return b.is_standing() and b.p1.x == self.goal.x and b.p1.y == self.goal.y

    def parse_terrain(self, level_file):
        """
        Parses the level file, initializes the boolean map of the Terrain object representing allowed traversable
        positions, sets up the start and goal postions based on location of S and T un the level file.
        :param level_file:
        """
        file = open(level_file, "r")
        self.map = []
        for x, line in enumerate(file):
            row = []
            for y, char in enumerate(line):
                if char == 'S':
                    self.start = Position(x, y)
                    row.append(True)
                elif char == 'T':
                    self.goal = Position(x, y)
                    row.append(True)
                elif char == '0':
                    row.append(True)
                elif char == 'X':
                    self.switchX = Position(x,y)
                    row.append(True)
                elif char == 'O':
                    self.switchO = Position(x,y)
                    row.append(True)
                elif char == 'H':
                    self.half_boards.append(Position(x,y))
                    row.append(True)
                elif char == '-':
                    row.append(False)
                elif char == 'A':
                    self.bridge_switchX.append(Position(x,y))
                    row.append(False)
                elif char == 'B':
                    self.bridge_switchO.append(Position(x,y))
                    row.append(False)
                elif char == 'C':
                    self.bridge_switchX.append(Position(x,y))
                    row.append(True)
                elif char == 'E':
                    self.switchE = Position(x,y)
                    row.append(True)
                elif char == 'F':
                    self.switchF = Position(x,y)
                    row.append(True)
                elif char == 'G':
                    self.switchG = Position(x,y)
                    row.append(True)
                elif char == 'K':
                    self.bridge_with_multi_switch.append(Position(x,y))
                    row.append(True)
            self.map.append(row)
        file.close()
        self.height = len(self.map)
        self.width = len(self.map[0])
        # print("Terrain map created")
        # print(json.dumps(self.map))

    def is_press_switchX(self, b :Block) -> bool:
        if not self.switchX:
            return False
        if self.switchX == b.p1 or self.switchX == b.p2:
            return True
        return False
    
    def is_press_switchE(self, b :Block) -> bool:
        if not self.switchE:
            return False
        if self.switchE == b.p1 or self.switchE == b.p2:
            return True
        return False
    
    def is_press_switchF(self, b :Block) -> bool:
        if not self.switchF:
            return False
        if self.switchF == b.p1 or self.switchF == b.p2:
            return True
        return False
    
    def is_press_switchG(self, b :Block) -> bool:
        if not self.switchG:
            return False
        if self.switchG == b.p1 or self.switchG == b.p2:
            return True
        return False
    
    def is_press_switchO(self, b :Block) -> bool:
        if not self.switchO:
            return False
        if self.switchO == b.p1 and self.switchO == b.p2:
            return True
        return False

    def __eq__(self, __o: object) -> bool:
        for row_index, row in enumerate(self.map):
            for col_index, item in enumerate(row):
                if self.map[row_index][col_index] != __o.map[row_index][col_index]:
                    return False
        return True