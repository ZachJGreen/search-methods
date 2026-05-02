import numpy as np
import random

EMPTY = 0
OBSTACLE = 1
START = 2
GOAL = 3
VISITED = 4
PATH = 5

class Grid:

    def __init__(self, size=15):
        if size < 5:
            raise ValueError("Maze size must be at least 5.")
        self.size = size
        self.cells = np.zeros((size, size), dtype=int)
        self.start = None
        self.goal = None

    def generate(self):
        self._generate_maze()
        self._place_start_and_goal()

    def _generate_maze(self):
        self.cells = np.full((self.size, self.size), OBSTACLE, dtype=int)

        start = (1, 1)
        stack = [start]
        self.cells[start[0]][start[1]] = EMPTY

        while stack:
            row, col = stack[-1]
            neighbors = self._unvisited_maze_neighbors(row, col)

            if not neighbors:
                stack.pop()
                continue

            next_row, next_col, wall_row, wall_col = random.choice(neighbors)
            self.cells[wall_row][wall_col] = EMPTY
            self.cells[next_row][next_col] = EMPTY
            stack.append((next_row, next_col))

    def _unvisited_maze_neighbors(self, row, col):
        directions = [(-2, 0), (2, 0), (0, 2), (0, -2)]
        neighbors = []

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 < nr < self.size - 1 and 0 < nc < self.size - 1:
                if self.cells[nr][nc] == OBSTACLE:
                    wall_row = row + dr // 2
                    wall_col = col + dc // 2
                    neighbors.append((nr, nc, wall_row, wall_col))

        return neighbors
                
    def _place_start_and_goal(self):
        empty_cells = self._get_empty_cells()
        if len(empty_cells) < 2:
            raise ValueError("Not enough maze corridors to place start and goal.")

        self.start = min(empty_cells)
        self.goal = max(
            empty_cells,
            key=lambda cell: (
                abs(cell[0] - self.start[0]) + abs(cell[1] - self.start[1]),
                cell[0],
                cell[1],
            ),
        )
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
