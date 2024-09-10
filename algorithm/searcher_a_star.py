from .searcher import Searcher, State
from typing import List, Tuple
from maze import Maze
import heapq

class SearcherAStar(Searcher):
    def __init__(self):
        super(SearcherAStar, self).__init__()
        self.pq : List[Tuple[int, State]]
        self.prevs : List[List[Tuple[int,int]]]
        self.min_costs : List[List[int]]
        self.is_init : bool
        self.reset()
    
    def reset(self) -> None:
        super(SearcherAStar, self).reset()
        self.pq = []
        self.prevs = []
        self.min_costs = []
        self.is_init = False

    def search(self, maze: Maze) -> List[Tuple[int, int]]:
        self.reset()
        self.__search_init(maze)

        while len(self.pq) > 0 and not self.is_finish:
            self.search_per_step(maze)

        return self.get_path()

    def backtrack(self, end) -> None:
        self.path = []
        cur_x, cur_y = end
        while (self.prevs[cur_x][cur_y] is not None):
            self.path.append(State(cur_x, cur_y, self.min_costs[cur_x][cur_y]))
            cur_x, cur_y=  self.prevs[cur_x][cur_y]

    def search_per_step(self, maze:Maze) -> bool:
        if self.is_finish:
            return True
        
        self.__search_init(maze)

        _, cur = heapq.heappop(self.pq)
        if (cur.x, cur.y) == maze.get_end():
            self.backtrack(maze.get_end())
            self.is_finish = True
            return self.is_finish
        
        if cur.cost_from_start > self.min_costs[cur.x][cur.y]:
            return self.is_finish   # skip expansion

        for next_x, next_y in maze.get_neighbors((cur.x, cur.y)):
            next_cost_from_start = cur.cost_from_start + maze.get_cost((next_x, next_y))
            if next_cost_from_start < self.min_costs[next_x][next_y]:
                # add to pq
                self.min_costs[next_x][next_y] = next_cost_from_start
                self.prevs[next_x][next_y] = (cur.x, cur.y)
                next_state = State(next_x, next_y, next_cost_from_start)
                next_heuristic = self.__heuristic((next_x, next_y), maze.get_end())
                heapq.heappush(self.pq, (next_heuristic, next_state))

        return self.is_finish

    def __heuristic(self, cur:Tuple[int,int], goal:Tuple[int,int]):
        f = abs(cur[0] - goal[0]) + abs(cur[1] - goal[1])   # L1 distance
        return f

    def __search_init(self, maze : Maze) -> None:
        if self.is_init: 
            return  # skip init if already done

        self.prevs = [[None] * maze.width for _ in range(maze.height)]
        self.min_costs = [[float('inf')] * maze.width for _ in range(maze.height)]

        start_x, start_y = maze.get_start()
        start_state = State(start_x, start_y, 0)
        
        self.min_costs[start_x][start_y] = 0
        heapq.heappush(self.pq, 
                        (self.__heuristic(maze.get_start(), maze.get_end()), start_state))

        self.is_init = True

    def get_searched(self) -> List[Tuple[int, int]]:
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
        for _, s in self.pq:
            pool_set.add((s.x, s.y))
        return list(pool_set)
