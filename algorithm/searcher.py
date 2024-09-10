
from abc import ABC, abstractmethod
from typing import List, Tuple
from maze import Maze

class State:
    def __init__(self, x : int, y : int, cost : int):
        self.x = x
        self.y = y
        self.cost_from_start = cost

    def __lt__(self, other):
        return self.cost_from_start < other.cost_from_start 

class Searcher(ABC):
    def __init__(self):
        self.path : List[State] = []
        self.is_finish : bool = False

    @abstractmethod
    def search(self, maze: Maze) -> List[Tuple[int, int]]:
        """
        Search for a path from start to end in the given maze.
        
        Args:
            maze (Maze): The maze to search.
        
        Returns:
            List[Tuple[int, int]]: A list of coordinates representing the path from start to end.
                                   Returns an empty list if no path is found.
        """
        pass

    def reset(self) -> None:
        """
        Reset the searcher to its initial state.
        """
        self.path = []
        self.is_finish = False

    @abstractmethod
    def search_per_step(self, maze : Maze) -> bool:
        # return Ture if search is finished, otherwise False
        return self.is_finish
    
    def get_path(self) -> List[Tuple[int, int]]:
        return [(s.x, s.y) for s in self.path]

    @abstractmethod
    def get_searched(self) -> List[Tuple[int, int]]:
        pass
    
    @abstractmethod
    def get_pool(self) -> List[Tuple[int, int]]:
        pass
    
    
