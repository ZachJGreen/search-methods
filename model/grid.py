import numpy as np
import random

EMPTY = 0
OBSTACLE = 1
START = 2
GOAL = 3
VISITED = 4
PATH = 5

class Grid:

    def __init__(self, size=10, obstacle_density=0.25):
        self.size = size
        self.obstacle_density = obstacle_density
        self.cells = np.zeros((size, size), dtype=int)
        self.start = None
        self.goal = None

    def generate(self):
        self.cells = np.zeros((self.size, self.size), dtype=int)
        self._place_obstacles()
        self._place_start_and_goal()
    
    def _place_obstacles(self):
        total_cells = self.size ** 2
        num_obstacles  = int(total_cells * self.obstacle_density)
        
        all_positions = [(r, c) for r in range(self.size) for c in range(self.size)]

        random.shuffle(all_positions)
        
        for r, c in all_positions[:num_obstacles]:
            self.cells[r][c] = OBSTACLE
                
    def _place_start_and_goal(self):
        empty_cells = self._get_empty_cells()
        if len(empty_cells) < 2:
            raise ValueError("Not enough empty cells. Try reducing obstacle density.")
        self.start, self.goal = random.sample(empty_cells, 2)
        self.cells[self.start[0]][self.start[1]] = START
        self.cells[self.goal[0]][self.goal[1]] = GOAL

    def _get_empty_cells(self):
        return [(r, c) for r in range(self.size) for c in range(self.size)
                if self.cells[r][c] == EMPTY]

    def is_traversable(self, row, col):
        if not self._in_bounds(row, col):
            return False
        return self.cells[row][col] != OBSTACLE

    def _in_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def get_neighbors(self, row, col):
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if self.is_traversable(nr, nc):
                neighbors.append((nr, nc))
        return neighbors

    def mark_visited(self, row, col):
        if self.cells[row][col] not in (START, GOAL):
            self.cells[row][col] = VISITED

    def mark_path(self, row, col):
        if self.cells[row][col] not in (START, GOAL):
            self.cells[row][col] = PATH

    def reset_search_state(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.cells[r][c] in (VISITED, PATH):
                    self.cells[r][c] = EMPTY