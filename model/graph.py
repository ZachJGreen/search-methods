import networkx as nx
from model.grid import OBSTACLE

class Graph:

    def __init__(self):
        self.graph = nx.Graph()

    def build_from_grid(self, grid):
        self.graph.clear()

        for r in range(grid.size):
            for c in range(grid.size):
                if grid.cells[r][c] != OBSTACLE:
                    self.graph.add_node((r, c))
        
        for r in range(grid.size):
            for c in range(grid.size):
                if grid.cells[r][c] != OBSTACLE:
                    for nr, nc in grid.get_neighbors(r, c):
                        self.graph.add_edge((r, c), (nr, nc))
    
    def get_neighbors(self, node):
        return list(self.graph.neighbors(node))
    
    def has_node(self, node):
        return self.graph.has_node(node)
    
    def is_connected(self, start, goal):
        if not self.has_node(start) or not self.has_node(goal):
            return False
        return nx.has_path(self.graph, start, goal)
    
    @property
    def node_count(self):
        return self.graph.number_of_nodes()
    
    @property
    def edge_count(self):
        return self.graph.number_of_edges()