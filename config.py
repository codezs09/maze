from dataclasses import dataclass
from typing import Tuple

@dataclass
class Config:
    # Searcher type
    SEARCHER_TYPE: str = "a_star"  # Options: "bfs", "dfs"(not implemented), "dijkstra", "a_star"

    # Maze dimensions
    MAZE_HEIGHT: int = 14
    MAZE_WIDTH: int = 16    

    # Visualization settings
    CELL_SIZE: int = 30
    DELAY: int = 1  # Milliseconds between each step in visualization

    # Maze generation
    OBSTACLE_DENSITY: float = 0.2  # Percentage of cells that are obstacles
    IS_SHOW_COST: bool = True

