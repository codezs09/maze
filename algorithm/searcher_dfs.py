from .searcher import State, Searcher
from maze import Maze
from typing import List, Tuple
from copy import deepcopy

class SearcherDFS(Searcher):
    def __init__(self):
        super(SearcherDFS, self).__init__()
        self.dfs_path : List[State]
        self.min_costs : List[List[int]]    # use this to prune unnecessary searchers
        self.is_init : bool
        self.reset()

    def reset(self) -> None:
        super(SearcherDFS, self).reset()
        self.dfs_path = []
        self.min_costs = []
        self.is_init = False

    def search(self, maze: Maze) -> List[Tuple[int, int]]:
        self.reset()
        self.__search_init(maze)

        start_x, start_y = maze.get_start()
        start_state = State(start_x, start_y, 0)

        self.min_costs[start_x][start_y] = 0

        dfs_traversal(start_state, maze)

    def dfs_traversal(self, cur : State, maze : Maze) -> None:
        if (cur.x, cur.y) == maze.get_end():
            if cur.cost_from_start < self.min_costs[cur.x][cur.y]:
                self.min_costs[cur.x][cur.y]
                self.path = deepcopy(self.dfs_path)
            return
        
        if cur.cost_from_start > self.min_costs[cur.x][cur.y]:
            return

        for next_x, next_y in maze.get_neighbors((cur.x, cur.y)):
            next_cost = cur.cost_from_start + maze.get_cost((next_x, next_y))
            if next_cost < self.min_costs[next_x][next_y]:
                next_state = State(next_x, next_y, next_cost)
                self.dfs_path.append(next_state)
                self.dfs_traversal(next_state)
                self.dfs_path.pop()

    def __search_init(self, maze : Maze):
        if self.is_init:
            return

        self.min_costs = [[float('inf')] * maze.width for _ in range(maze.height)]
        
        self.is_init = True
