import networkx as nx
from collections import deque


class TreeView:
    """
    Draws the search tree (inverted: root at top, children below).

    Nodes are positioned with a simple level-order layout:
      - y = -depth  (root at y=0, children progressively lower)
      - x = evenly spaced within each depth level

    Colour scheme
    -------------
    Green  (#4CAF50) – root / start node
    Red    (#F44336) – goal node
    Orange (#FF9800) – node currently being expanded
    Blue   (#64B5F6) – frontier (queued but not yet expanded)
    Yellow (#FFC107) – nodes on the final path
    Grey   (#B0BEC5) – already visited / expanded
    """

    def __init__(self, ax):
        self.ax = ax
        self.tree = nx.DiGraph()
        self.root = None
        self.goal = None
        self._levels = {}          # node -> depth
        self._level_nodes = {}     # depth -> [node, …] in insertion order

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def reset(self, root, goal=None):
        self.tree.clear()
        self.root = root
        self.goal = goal
        self._levels = {root: 0}
        self._level_nodes = {0: [root]}
        self.tree.add_node(root)

    def add_node(self, node, parent):
        """Add *node* as a child of *parent* in the search tree."""
        if node in self.tree:
            return
        depth = self._levels[parent] + 1
        self._levels[node] = depth
        self._level_nodes.setdefault(depth, []).append(node)
        self.tree.add_node(node)
        self.tree.add_edge(parent, node)

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _compute_positions(self):
        """Return {node: (x, y)} with a simple level-order layout."""
        pos = {}
        for depth, nodes in self._level_nodes.items():
            n = len(nodes)
            for i, node in enumerate(nodes):
                x = (i + 0.5) / n   # 0 … 1
                y = -depth
                pos[node] = (x, y)
        return pos

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, current=None, frontier=None, path=None):
        self.ax.clear()
        self.ax.set_title("Search Tree", fontsize=11, fontweight="bold")
        self.ax.axis("off")

        if not self.tree.nodes:
            return

        frontier = set(frontier) if frontier else set()
        path_set = set(path) if path else set()

        pos = self._compute_positions()

        max_depth = max(self._levels.values()) if self._levels else 0

        # --- edges ---
        for parent, child in self.tree.edges():
            if parent not in pos or child not in pos:
                continue
            x1, y1 = pos[parent]
            x2, y2 = pos[child]
            on_path = parent in path_set and child in path_set
            color = "#FFC107" if on_path else "#CCCCCC"
            lw = 2.0 if on_path else 0.6
            self.ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw,
                         zorder=1, solid_capstyle='round')

        # --- nodes ---
        for node in self.tree.nodes():
            if node not in pos:
                continue
            x, y = pos[node]

            if node == current:
                color = "#FF9800"
                size = 220
                zorder = 5
            elif path_set and node in path_set:
                color = "#FFC107"
                size = 160
                zorder = 4
            elif node == self.goal:
                color = "#F44336"
                size = 160
                zorder = 4
            elif node == self.root:
                color = "#4CAF50"
                size = 160
                zorder = 4
            elif node in frontier:
                color = "#64B5F6"
                size = 100
                zorder = 3
            else:
                color = "#B0BEC5"
                size = 80
                zorder = 2

            self.ax.scatter(x, y, s=size, c=color, zorder=zorder,
                            edgecolors="#555555", linewidths=0.4)

            # Labels only for notable nodes; skip for crowded trees
            label = None
            if node == self.root:
                label = "S"
            elif node == self.goal:
                label = "G"
            elif node == current and node not in (self.root, self.goal):
                label = "▶"

            if label:
                self.ax.text(x, y, label, ha='center', va='center',
                             fontsize=7, fontweight='bold', color='white',
                             zorder=zorder + 1)

        # --- axis limits ---
        if pos:
            xs = [p[0] for p in pos.values()]
            ys = [p[1] for p in pos.values()]
            pad_x = max(0.1, 0.5 / max(len(pos), 1))
            self.ax.set_xlim(min(xs) - pad_x, max(xs) + pad_x)
            self.ax.set_ylim(min(ys) - 0.6, max(ys) + 0.6)

        # --- depth legend on right side ---
        if max_depth > 0:
            self.ax.text(
                1.0, 0, f"depth {max_depth}",
                transform=self.ax.transAxes,
                ha='right', va='bottom', fontsize=7, color='#888888'
            )
