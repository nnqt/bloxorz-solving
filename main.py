#  Copyright (c) 2020. Abhilshit Soni

from app.block import Block
from app.move import Move
from app.terrain import Terrain
from app.a_star_solver import A_Star_Solver
from app.breadth_first_search import Breadth_First_Search
from app.monte_carlo_tree_search import Monte_Carlo_Tree_Search
import time
import json

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


class Game:
    """
       A Game class that is responsible for building a game from the terrain information obtained from a level file.
        It also has a reference to A* Solver Agent  which can search the path to obtain a solution
    """
    def __init__(self, terrain):
        """
        Initializes a Game Object with a terrain that is constructed based on a level file
        :param terrain:
        """
        self.terrain = terrain
        #self.a_star_solver_agent = A_Star_Solver(h_func="Eucledian")
        self.a_star_solver_agent =  A_Star_Solver(h_func="Chebyshev")
        self.breadth_first_search_solver_agent =Breadth_First_Search()
        self.monte_carlo_tree_search_agent = Monte_Carlo_Tree_Search()
        

    def solve_game(self, choise):
        start_time = time.time()
        if(choise == 1):
            paths = self.breadth_first_search_solver_agent.solve(self.terrain)
            fig = px.line(self.breadth_first_search_solver_agent.data_all_queue)
        elif(choise == 2):
            paths = self.a_star_solver_agent.solve(self.terrain)
            fig = px.line(self.a_star_solver_agent.data_all_queue)
        elif(choise == 3):
            paths = self.monte_carlo_tree_search_agent.solve(self.terrain)
            fig = px.line(self.monte_carlo_tree_search_agent.data_open_queue)
        else:
            return
        print("")
        print("--- Solved using A* in %s seconds ---" % (time.time() - start_time))
        print("Solution: ", self.pretty_print_paths(paths))

        fig.show()

    def pretty_print_paths(self, paths):
        """
        Accepts a list of @Move object representing moves taken to reach to the goal from start and
        returns a pretty printed string represnting the sequence of moves required to reach the goal from start state
        :param paths:
        :return: String of pretty printed path
        """
        path_str = ""
        for i, path in enumerate(paths):
            if path is None:
                continue
            elif path == Move.Right:
                path_str = path_str + " Right "
            elif path == Move.Left:
                path_str = path_str + " Left "
            elif path == Move.Down:
                path_str = path_str + " Down "
            elif path == Move.Up:
                path_str = path_str + " Up "
            if i < len(paths) - 1:
                path_str = path_str + "->"

        return path_str
    
def input_level():
    print("")
    print("############### Choosen level ############")
    print("Level between 1 and 7:")
    level_choise = int(input(""))
    if level_choise < 1 or level_choise > 7:
        print("Out of range!")
        print("############### Again!!! ###############")
        level_choise = input_level()
    return level_choise

def input_algorithms():
    print("")
    print("1. Breadth First Search")
    print("2. A Star Search")
    print("3. Monte Carlo Tree Search")
    algorithms_choise = int(input(""))
    if algorithms_choise < 1 or algorithms_choise > 3:
        print("Out of range!")
        print("############### Again!!! ###############")
        algorithms_choise = input_algorithms()
    return algorithms_choise

if __name__ == '__main__':
    # Input level
    level_choise = input_level()
    #level_choise = 1
    
    # Initialize terrain
    path_file = "resources/level0" + str(level_choise) + ".txt"
    terrain = Terrain(level_file=path_file)
    print("")
    print("Start at:" + str(terrain.start))
    print("Goal at:" + str(terrain.goal))
    print("")

    # Input algorithms
    algorithms_choise = input_algorithms()
    #algorithms_choise = 3

    # Create Game
    game = Game(terrain)
    #Solve Game by finding sequence path of moves required to reach to goal from start
    game.solve_game(algorithms_choise)