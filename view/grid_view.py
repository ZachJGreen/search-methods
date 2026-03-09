import matplotlib.pyplot as plt
import matplotlib.patches as patches
from model.grid import EMPTY, OBSTACLE, START, GOAL, VISITED, PATH

CELL_COLORS = {
    EMPTY: "#FFFFFF",
    OBSTACLE: "#2C2C2C",
    START: "#4CAF50",
    GOAL: "#F44336",
    VISITED: "#90CAF9",
    PATH: "#FFC107"
}

class GridView:

    def __init__(self, ax):
        self.ax = ax

    def draw(self, grid):
        self.ax.clear()
        self.ax.set_title("2D Grid", fontsize=12, fontweight="bold")
        self.ax.set_xlim(0, grid.size)
        self.ax.set_ylim(0, grid.size)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        for r in range(grid.size):
            for c in range(grid.size):
                cell_value = grid.cells[r][c]
                color = CELL_COLORS.get(cell_value, "#FFFFFF")

                rect = patches.Rectangle(
                    (c, grid.size - 1 - r),
                    1, 1,
                    linewidth=0.5,
                    edgecolor="#CCCCCC",
                    facecolor=color
                )
                self.ax.add_patch(rect)

                if cell_value == START:
                    self._draw_label(c, grid.size - 1 - r, "S")
                elif cell_value == GOAL:
                    self._draw_label(c, grid.size - 1 - r, "G")
    
    def _draw_label(self, col, row, text):
        self.ax.text(
            col + 0.5, row + 0.5, text,
            ha="center", va="center",
            fontsize=10, fontweight="bold", color="white"
        )
    
