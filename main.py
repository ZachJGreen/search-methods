from model.grid import Grid
from model.graph import Graph
from view.grid_view import GridView

import matplotlib.pyplot as plt
import argparse


def main(size: int = 10, density: float = 0.25):
    grid = Grid(size=size, obstacle_density=density)
    grid.generate()

    graph = Graph()
    graph.build_from_grid(grid)

    print(f"Grid size: {grid.size}x{grid.size}")
    print(f"Obstacles density: {grid.obstacle_density}")
    print(f"Graph nodes: {graph.node_count}, edges: {graph.edge_count}")

    fig, ax = plt.subplots(figsize=(6, 6))
    view = GridView(ax)
    view.draw(grid)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run grid + graph demo")
    parser.add_argument("--size", type=int, default=10, help="Grid size (NxN)")
    parser.add_argument("--density", type=float, default=0.25, help="Obstacle density (0-1)")
    args = parser.parse_args()
    main(size=args.size, density=args.density)
