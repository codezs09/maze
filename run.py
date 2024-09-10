from maze import Maze
from visualizer import MazeVisualizer
from config import Config
from algorithm.searcher_factory import SearcherFactory

def run():
    # Instantiate the maze according to the config
    maze = Maze(height=Config.MAZE_HEIGHT, width=Config.MAZE_WIDTH, \
                is_rand_start_goal=True)

    # Instantiate the searcher using the factory
    searcher = SearcherFactory.create_searcher(Config.SEARCHER_TYPE)

    # Initiate the searching
    path = searcher.search(maze)

    maze_visualizer = MazeVisualizer(maze)
    maze_visualizer.update()
    maze_visualizer.mark_path(path)
    maze_visualizer.update()
    maze_visualizer.show()

def run_by_steps():
    # Instantiate the maze according to the config
    maze = Maze(height=Config.MAZE_HEIGHT, width=Config.MAZE_WIDTH, \
                is_rand_start_goal=True)

    # Instantiate the searcher using the factory
    searcher = SearcherFactory.create_searcher(Config.SEARCHER_TYPE)

    maze_visualizer = MazeVisualizer(maze)
    maze_visualizer.update()

    while not searcher.search_per_step(maze):
        maze_visualizer.redraw_canvas()
        maze_visualizer.mark_searched(searcher.get_searched())
        maze_visualizer.mark_pool(searcher.get_pool())
        maze_visualizer.update()

    maze_visualizer.redraw_canvas()
    maze_visualizer.mark_path(searcher.get_path())
    maze_visualizer.update()
    maze_visualizer.show()

if __name__ == "__main__":
    # run()
    run_by_steps()


