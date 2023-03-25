#  Copyright (c) 2020. Abhilshit Soni

import json


class Position:
    """
    A position object depicting position on terrain map.
    """
    def __init__(self, x, y):
        """
        Initialize position based on column (x) row(y)
        :param x:
        :param y:
        """
        self.x = x
        self.y = y

    def dx(self, d):
        """
        Utility function to shift x by a certain distance d
        :param d:
        :return:
        """
        return Position(self.x + d, self.y)

    def dy(self, d):
        """
           Utility function to shift x by a certain distance d
           :param d:
           :return:
        """
        return Position(self.x, self.y + d)

    def __str__(self):
        return json.dumps([self.x, self.y])
    
    def __eq__(self, __o) -> bool:
        if self.x == __o.x and self.y == __o.y:
            return True
        else: 
            return False
