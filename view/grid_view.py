import matplotlib.patches as patches
from model.grid import EMPTY, OBSTACLE, START, GOAL, VISITED, PATH

CELL_COLORS = {
    EMPTY:    "#FFFFFF",
    OBSTACLE: "#2C2C2C",
    START:    "#4CAF50",
    GOAL:     "#F44336",
    VISITED:  "#90CAF9",
    PATH:     "#FFC107",
}


class GridView:

    def __init__(self, ax):
        self.ax = ax

    def draw(self, grid, current_agent=None, perception=None):
        """
        Draw the 2-D grid.

        Parameters
        ----------
        grid           : Grid  – the model to render
        current_agent  : (row, col) | None  – agent's current position
                         drawn as an orange circle overlay
        perception     : list[(row, col)] | None  – cells the agent can
                         currently "see" (current + 4 neighbours);
                         drawn with a dashed highlight border
        """
        self.ax.clear()
        self.ax.set_title("Maze Grid", fontsize=12, fontweight="bold")
        self.ax.set_xlim(0, grid.size)
        self.ax.set_ylim(0, grid.size)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        perception_set = set(perception) if perception else set()

        for r in range(grid.size):
            for c in range(grid.size):
                cell_value = grid.cells[r][c]
                color = CELL_COLORS.get(cell_value, "#FFFFFF")

                # base cell rectangle
                rect = patches.Rectangle(
                    (c, grid.size - 1 - r), 1, 1,
                    linewidth=0.5,
                    edgecolor="#CCCCCC",
                    facecolor=color,
                    zorder=1,
                )
                self.ax.add_patch(rect)

                # perception highlight: dashed border
                if (r, c) in perception_set:
                    perc_rect = patches.Rectangle(
                        (c + 0.05, grid.size - 1 - r + 0.05), 0.9, 0.9,
                        linewidth=1.2,
                        edgecolor="#FF9800",
                        facecolor="none",
                        linestyle="--",
                        zorder=3,
                    )
                    self.ax.add_patch(perc_rect)

                # labels for start / goal
                if cell_value == START:
                    self._draw_label(c, grid.size - 1 - r, "S")
                elif cell_value == GOAL:
                    self._draw_label(c, grid.size - 1 - r, "G")

        # agent position overlay (orange circle)
        if current_agent is not None:
            r, c = current_agent
            self.ax.plot(
                c + 0.5, grid.size - 1 - r + 0.5,
                marker='o', markersize=10,
                color='#FF9800', markeredgecolor='#333333',
                markeredgewidth=0.8,
                zorder=5,
            )

    def _draw_label(self, col, row, text):
        self.ax.text(
            col + 0.5, row + 0.5, text,
            ha="center", va="center",
            fontsize=10, fontweight="bold", color="white",
            zorder=4,
        )
