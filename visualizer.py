
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
from maze import Maze
from config import Config

class MazeVisualizer:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.im = None
        self.setup_plot()

    def setup_plot(self):
        # Create a custom colormap with black for obstacles and YlOrBr for costs
        self.colors = ['black'] + plt.cm.YlOrBr(np.linspace(0, 1, 11)).tolist()
        self.cmap = ListedColormap(self.colors)

        # Convert maze to numpy array for visualization
        self.maze_array = np.array(self.maze.matrix).astype(float)
        
        if not Config.IS_SHOW_COST:
            # Set all non-negative values to 0
            self.maze_array[self.maze_array >= 0] = 0

        self.__draw_maze()
        self.fig.colorbar(self.im, ax=self.ax, label='Cost')

    def __draw_maze(self):
        self.im = self.ax.imshow(self.maze_array, cmap=self.cmap, vmin=-1, vmax=len(self.colors)-2)

        # Mark start cell with a circle
        start_y, start_x = self.maze.start
        self.ax.plot(start_x, start_y, 'bo', markersize=10, markeredgecolor='white')
        
        # Mark end cell with a cross
        end_y, end_x = self.maze.end
        self.ax.plot(end_x, end_y, 'rx', markersize=10, markeredgewidth=2)

        plt.tight_layout()

    def mark_searched(self, cells):
        for y, x in cells:
            if self.maze_array[y, x] != -1:  # Mark if it's not an obstacle
                rect = matplotlib.patches.Rectangle((x-0.5, y-0.5), 1, 1, fill=True, facecolor='grey', edgecolor='none', alpha=0.6)
                self.ax.add_patch(rect)

    def mark_pool(self, cells):
        for y, x in cells:
            if self.maze_array[y,x] != -1:
                rect = matplotlib.patches.Rectangle((x-0.5, y-0.5), 1, 1, fill=True, facecolor='blue', edgecolor='none', alpha=0.6)
                self.ax.add_patch(rect)

    def mark_path(self, path):
        for y, x in path:
            rect = matplotlib.patches.Rectangle((x-0.5, y-0.5), 1, 1, fill=True, facecolor='green', edgecolor='none', alpha=0.6)
            self.ax.add_patch(rect)

    def redraw_canvas(self):
        self.ax.clear()
        self.__draw_maze()

    def update(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(Config.DELAY / 1000)  # Convert milliseconds to seconds

    def show(self):
        plt.show()
