
# Generate a maze (represented by 2D array)
# with negative values (-1) as obstacles and positive ones as cost to move to this cell
# the goal is to find the path from start to end with the lowest cost

import random
from typing import Tuple, List
from config import Config

class Maze:
    def __init__(self, height : int = 20, width : int = 50, is_rand_start_goal : bool = False) -> None:
        self.height = height
        self.width = width
        self.matrix = [[0] * self.width for _ in range(self.height)]
        self.generate_maze()
        if is_rand_start_goal:
            self.__random_start_target()
        else:
            self.start = (0, 0)
            self.end = (self.height - 1, self.width - 1)

    def generate_maze(self) -> None:
        # generate random obstacles
        for i in range(self.height):
            for j in range(self.width):
                if random.random() < Config.OBSTACLE_DENSITY:
                    self.matrix[i][j] = -1
        
        # generate random cost for each cell
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][j] != -1:
                    self.matrix[i][j] = random.randint(1, 10)

    def __random_start_target(self): 
        x, y = self.__random_xy()
        while self.matrix[x][y] < 0 or len(self.get_neighbors((x,y))) == 0:
            x, y = self.__random_xy()
        self.start = (x, y)

        x, y = self.__random_xy()
        while self.matrix[x][y] < 0 or len(self.get_neighbors((x,y))) == 0 or \
            (x, y) == self.start:
            x, y = self.__random_xy()
        self.end = (x, y)

    def __random_xy(self):
        x = random.randint(0, self.height-1)
        y = random.randint(0, self.width-1)
        return (x, y)

    def get_start(self) -> Tuple[int, int]:
        return self.start

    def get_end(self) -> Tuple[int, int]:
        return self.end

    def set_start(self, start : Tuple[int, int]) -> None:
        self.start = start

    def set_end(self, end : Tuple[int, int]) -> None:
        self.end = end

    def get_neighbors(self, pos : Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbors = []
        if 0 <= pos[0] < self.height and 0 <= pos[1] < self.width and \
            self.matrix[pos[0]][pos[1]] >= 0:
            moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for move in moves:
                new_x = pos[0] + move[0]
                new_y = pos[1] + move[1]
                if 0 <= new_x < self.height and 0 <= new_y < self.width and \
                    self.matrix[new_x][new_y] >= 0:
                    neighbors.append((new_x, new_y))
        return neighbors

    def get_cost(self, pos : Tuple[int, int]) -> int:
        return self.matrix[pos[0]][pos[1]]

if __name__ == "__main__":
    from visualizer import MazeVisualizer
    maze = Maze(height = 5, width = 10)
    maze_visualizer = MazeVisualizer(maze)
    maze_visualizer.update()
    maze_visualizer.mark_searched([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)])
    maze_visualizer.update()
    maze_visualizer.mark_path([(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)])
    maze_visualizer.update()
    maze_visualizer.show()
    