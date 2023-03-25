from app.block import Block
from app.node import Node
from app.terrain import Terrain

import math
import random
import copy
import time

class Monte_Carlo_Tree_Search:
    def __init__(self) :
        self.data_open_queue = []
        self.data_all_queue = []
        self.open_list = []
    
    def solve(self, terrain:Terrain) -> list:

        # Init root node
        start_pos = terrain.start
        start_block = Block(start_pos, start_pos)
        start_node = Node(start_block, move=None, parent=None, f=0, g=0, h=0, terrain=terrain)

        self.open_list.append(start_node)
        current_node = self.open_list[0]

        # Use MCTS to find leaf node
        while current_node is not None:
            if current_node.terrain.done(current_node.block):
                break
            current_node = self.monte_carlo_tree_search(current_node)
            print( "Ta chon " + str(current_node.move))
            print("")
            self.open_list.append(current_node)
            self.data_open_queue.append(len(self.open_list))

        if current_node is None:
            print("Fail")
            return ""
        # BackTrack Moves
        path = []
        current = current_node
        while current is not None:
            path.append(current.move)
            current = current.parent
        return path[::-1] # Return reversed order of Moves

    def monte_carlo_tree_search(self, current_node: Node) -> Node:
        visited_list = []

        timeout = 5
        timeout_start = time.time()
        #for x in range(10):
        while time.time() < timeout_start + timeout:
            leaf = self.traverse(current_node, visited_list) # Selection
            if leaf not in visited_list:
                visited_list.append(leaf)
            if leaf is None:
                simulation_result = 0
            else:
                simulation_result = self.rollout(leaf) # Simulation
            self.backpropagate(leaf, result= simulation_result) # Backpropagation
        print("------------------")
        for x in visited_list:
            if x:
                print("Lua chon: " + str(x.move) + " co ti le win la: " + str(x.reward) + " duoc duyet qua: " + str(x.n) + " lan")
            else:
                print("Khong tim duoc duong di")
        return self.best_child(visited_list)
    
    def traverse(self, current_node: Node, visited_list: list) -> Node:
        children = self.get_children(current_node)
        unvisited_node = None
        best_uct_node = None
        for child in children:
            if current_node.parent is not None:
                if child == current_node.parent:
                    children.remove(child)
            # if child in self.open_list:
            #     children.remove(child)
        for child in children:
            if child not in visited_list:
                unvisited_node = child
                break
        if not unvisited_node:
            best_uct_node = self.best_uct(visited_list)
            # if best_uct_node is None:
            #     return None
        return unvisited_node or best_uct_node

    def rollout(self, node: Node) -> Node:
        count = 0
        result = 0
        time_out = 0.1
        h = abs(node.block.p1.x - node.terrain.goal.x) + abs(node.block.p1.y - node.terrain.goal.y)
        if h == 0:
            h = 1
        k = 200 * math.log(h) + 1

        time_start = time.time()
        log_list = copy.deepcopy(self.open_list)
        log_list.append(node)
        #while time.time() < time_start + time_out:
        while count < k:
            if node.terrain.done(node.block):
                result = 1
                break
            node = self.rollout_policy(node=node, log_list=log_list)
            log_list.append(node)
            if node is None:
                break
            count += 1
        
        return result


    def rollout_policy(self, node: Node, log_list: list) -> Node:
        children = self.get_children(node)
        for child in children:
            if child == node.parent:
            #if child in self.open_list:
                children.remove(child)
        if not children:
            return None
        #result = []
        # for child in children:
        #     if child in log_list:
        #         continue
        #     result.append(child)
        #if not result:
        #    return None
        #return random.choice(result + result)
        return random.choice(children + children)
        

    def backpropagate(self, node: Node, result) -> None:
        if node is None:
            return
        node.reward += result
        node.n += 1
        node.q = node.reward / node.n
        self.backpropagate(node.parent, result=result)


    def best_child(self, visited_list :list) -> Node:
        max = 0
        max_index = 0
        if not visited_list:
            return None
        for index, child in enumerate(visited_list):
            if max < child.n:
                max = child.n
                max_index = index
        return visited_list[max_index]

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
            child = Node(block=legal_neighbour, move=legal_move, parent=current_node, terrain = new_terrain, n = 0)
            children.append(child)
        return children
    
    def best_uct(self, visited_list:list) -> Node:
        index_max = 0
        max = 0
        for x, child in enumerate(visited_list):
            uct = self.calculate_uct(child)
            if max < uct:
                index_max = x
                max = uct
        if not visited_list:
            return None
        return visited_list[index_max]

    def calculate_uct(self, node: Node) :
        #root = self.open_list[0]

        w = node.reward
        n = node.n
        n_root = node.parent.n
        q = node.q
        c = 1
        x = math.sqrt((math.log(n_root, math.e)) / n)
        #c = math.sqrt(2)
        #x = math.sqrt(n_root) / (1 + n)
        result = q + (c * x)
        return result
