from collections import deque


class SearchAgent:
    """
    Uninformed search agent operating on a Grid + Graph.

    Perception is limited to the current node and its 4 cardinal neighbours.
    Supported methods: BFS (breadth-first) and DFS (depth-first).
    """

    def __init__(self, grid, graph):
        self.grid = grid
        self.graph = graph
        self.states_searched = 0
        self.found = False
        self.path = []

    # ------------------------------------------------------------------
    # Perception
    # ------------------------------------------------------------------

    def perceive(self, node):
        """
        Return the agent's local view: the current node and its traversable
        4-cardinal neighbours.  This is the *only* information the agent uses
        when deciding which nodes to add to the frontier.
        """
        r, c = node
        neighbors = self.grid.get_neighbors(r, c)
        return node, neighbors

    # ------------------------------------------------------------------
    # BFS
    # ------------------------------------------------------------------

    def bfs_steps(self):
        """
        Generator that advances BFS one expansion at a time.

        Each yield is a dict with keys:
          type          – 'step' | 'found' | 'no_path'
          node          – node just expanded (or goal when found)
          new_children  – list of nodes added to the frontier this step
          frontier      – snapshot of the current frontier (list)
          parent        – parent-pointer dict (full)
          path          – reconstructed path (only on 'found')
        """
        start = self.grid.start
        goal = self.grid.goal

        queue = deque([start])
        visited = {start}
        parent = {start: None}

        while queue:
            node = queue.popleft()
            self.states_searched += 1

            # --- perception: agent only sees current + cardinal neighbours ---
            _, neighbors = self.perceive(node)

            if node == goal:
                self.found = True
                self.path = self._reconstruct_path(goal, parent)
                yield {
                    'type': 'found',
                    'node': node,
                    'new_children': [],
                    'frontier': list(queue),
                    'parent': parent,
                    'path': self.path,
                }
                return

            new_children = []
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    queue.append(neighbor)
                    new_children.append(neighbor)

            yield {
                'type': 'step',
                'node': node,
                'new_children': new_children,
                'frontier': list(queue),
                'parent': parent,
            }

        yield {
            'type': 'no_path',
            'node': None,
            'new_children': [],
            'frontier': [],
            'parent': parent,
            'path': [],
        }

    # ------------------------------------------------------------------
    # DFS
    # ------------------------------------------------------------------

    def dfs_steps(self):
        """
        Generator that advances DFS one expansion at a time.
        Nodes are marked visited when *pushed* to avoid duplicate expansions.
        """
        start = self.grid.start
        goal = self.grid.goal

        stack = [start]
        visited = {start}
        parent = {start: None}

        while stack:
            node = stack.pop()
            self.states_searched += 1

            # --- perception ---
            _, neighbors = self.perceive(node)

            if node == goal:
                self.found = True
                self.path = self._reconstruct_path(goal, parent)
                yield {
                    'type': 'found',
                    'node': node,
                    'new_children': [],
                    'frontier': list(stack),
                    'parent': parent,
                    'path': self.path,
                }
                return

            new_children = []
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    stack.append(neighbor)
                    new_children.append(neighbor)

            yield {
                'type': 'step',
                'node': node,
                'new_children': new_children,
                'frontier': list(stack),
                'parent': parent,
            }

        yield {
            'type': 'no_path',
            'node': None,
            'new_children': [],
            'frontier': [],
            'parent': parent,
            'path': [],
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _reconstruct_path(self, goal, parent):
        path = []
        node = goal
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path
