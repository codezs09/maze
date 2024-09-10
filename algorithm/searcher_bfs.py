from .searcher import Searcher, State
from maze import Maze
from typing import List, Tuple
from collections import deque

class SearcherBFS(Searcher):
    def __init__(self):
        super(SearcherBFS, self).__init__()
        self.q : deque[State]
        self.prevs : List[List[Tuple[int, int]]]
        self.min_costs : List[List[int]]
        self.is_init : bool
        self.reset()

    def reset(self) -> None:
        super(SearcherBFS, self).reset()
        self.q = deque()
        self.prevs = []
        self.min_costs = []
        self.is_init = False

    def search(self, maze: Maze) -> List[Tuple[int, int]]:
        self.reset()
        self.__search__init(maze)

        while len(self.q) > 0 and not self.is_finish:
            self.search_per_step(maze)

        self.is_finish = True
        return self.get_path()

    def backtrack(self, end) -> None:
        self.path = []
        cur_x, cur_y = end
        while (self.prevs[cur_x][cur_y] is not None):
            self.path.append(State(cur_x, cur_y, self.min_costs[cur_x][cur_y]))
            cur_x, cur_y=  self.prevs[cur_x][cur_y]

    def search_per_step(self, maze : Maze) -> bool:
        if self.is_finish:
            return True     # skip, search is already done

        self.__search__init(maze)

        if len(self.q) == 0:
            self.is_finish = True
            return self.is_finish

        cur = self.q.popleft()
        print(f"cur ({cur.x}, {cur.y}, cost-from-start is {cur.cost_from_start})")

        goal_x, goal_y = maze.get_end()

        if cur.cost_from_start > self.min_costs[cur.x][cur.y] or \
            cur.cost_from_start > self.min_costs[goal_x][goal_y]:
            return self.is_finish   # no need to expand from current node

        if (cur.x, cur.y) == (goal_x, goal_y):
            self.backtrack(maze.get_end())
            return self.is_finish

        for next_x, next_y in maze.get_neighbors((cur.x, cur.y)):
            next_cost = cur.cost_from_start + maze.get_cost((next_x, next_y))
            if next_cost < self.min_costs[next_x][next_y] and \
                next_cost < self.min_costs[goal_x][goal_y]:
                self.min_costs[next_x][next_y] = next_cost
                self.prevs[next_x][next_y] = (cur.x, cur.y)
                self.q.append(State(next_x, next_y, next_cost))
        
        return self.is_finish

    def __search__init(self, maze : Maze) -> None:
        if self.is_init:
            return  # skip init if already done

        self.prevs = [[None]*maze.width for _ in range(maze.height)]
        self.min_costs = [[float('inf')]*maze.width for _ in range(maze.height)]
        
        start_x, start_y = maze.get_start()
        start_state = State(start_x, start_y, 0)

        self.min_costs[start_x][start_y] = 0
        self.q.append(start_state)

        self.is_init = True

    def get_searched(self) -> List[Tuple[int,int]]:
        searched = []
        height = len(self.min_costs)
        for x in range(height):
            width = len(self.min_costs[0])
            for y in range(width):
                if self.min_costs[x][y] < float('inf'):
                    searched.append((x,y))
        return searched

    def get_pool(self) -> List[Tuple[int, int]]:
        pool_set = set()
        for s in self.q:
            pool_set.add((s.x, s.y))
        return list(pool_set)