#from math import sqrt

from app.block import Block
from app.node import Node
from app.terrain import Terrain

class Breadth_First_Search:
    def __init__(self):
        self.data_open_queue = []
        self.data_all_queue = []

    def solve(self, terrain:Terrain) -> list:
        open_list = []  # Initialize open list
        closed_list = []  # Initialize closed list

        start_pos = terrain.start
        start_block = Block(start_pos, start_pos)
        start_node = Node(start_block, move=None, parent=None, f=0, g=0, h=0, terrain=terrain) #Initialize a start Node object

        open_list.append(start_node) #add start Node to the open list
        while len(open_list) > 0:
            # Get the current node
            current_node = open_list[0]
            
            open_list.pop(0)
            closed_list.append(current_node)
            if current_node.terrain.done(current_node.block):
                path = []
                current = current_node
                # BackTrack Moves
                while current is not None:
                    path.append(current.move)
                    current = current.parent
                return path[::-1]  # Return reversed order of Moves
            children = self.get_children(current_node)

            for child in children:
                # continue if child is on the closed list
                if child in closed_list:
                    continue

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node:
                        continue

                # Add the child to the open list
                open_list.append(child)
            self.data_open_queue.append(len(open_list))
            self.data_all_queue.append(len(open_list) + len(closed_list))
        return ""

    def get_children(self, current_node: Node):
        """
        Gets Children of current Node by querying legal neighbours of a node block.
        :param current_node:
        :param terrain:
        :return:
        """
        legal_neighbours = current_node.terrain.legal_neighbors(current_node.block)
        children = []
        for (legal_neighbour, legal_move, new_terrain) in legal_neighbours:
            child = Node(block=legal_neighbour, move=legal_move, parent=current_node, terrain = new_terrain)
            children.append(child)
        return children

