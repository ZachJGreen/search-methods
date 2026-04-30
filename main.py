import argparse
import matplotlib.pyplot as plt

from model.grid import Grid
from model.graph import Graph
from controller.search import SearchAgent
from view.grid_view import GridView
from view.tree_view import TreeView


def main(size: int = 10, density: float = 0.25,
         method: str = 'bfs', delay: float = 0.15):

    # ------------------------------------------------------------------ #
    # 1. Build the state space
    # ------------------------------------------------------------------ #
    grid = Grid(size=size, obstacle_density=density)
    grid.generate()

    graph = Graph()
    graph.build_from_grid(grid)

    print(f"Grid      : {size}x{size}")
    print(f"Obstacles : {density:.0%}")
    print(f"Nodes     : {graph.node_count}  |  Edges: {graph.edge_count}")
    print(f"Start     : {grid.start}  |  Goal: {grid.goal}")
    print(f"Method    : {method.upper()}")
    print("-" * 40)

    # ------------------------------------------------------------------ #
    # 2. Set up the figure (grid view left, search-tree view right)
    # ------------------------------------------------------------------ #
    fig, (ax_grid, ax_tree) = plt.subplots(
        1, 2,
        figsize=(14, 7),
        gridspec_kw={'width_ratios': [1, 1.4]},
    )
    fig.patch.set_facecolor("#F5F5F5")
    plt.tight_layout(pad=2.5)

    grid_view = GridView(ax_grid)
    tree_view = TreeView(ax_tree)

    # ------------------------------------------------------------------ #
    # 3. Create and initialise the search agent
    # ------------------------------------------------------------------ #
    agent = SearchAgent(grid, graph)
    tree_view.reset(grid.start, goal=grid.goal)

    # initial frame
    grid_view.draw(grid, current_agent=grid.start)
    tree_view.draw(current=grid.start)
    plt.tight_layout(pad=2.5)
    plt.pause(0.6)

    # ------------------------------------------------------------------ #
    # 4. Animate the search
    # ------------------------------------------------------------------ #
    plt.ion()

    steps = agent.bfs_steps() if method == 'bfs' else agent.dfs_steps()
    final_state = None

    for state in steps:
        node       = state.get('node')
        new_kids   = state.get('new_children', [])
        frontier   = state.get('frontier', [])
        parent_map = state.get('parent', {})
        step_type  = state['type']

        # add newly discovered nodes to the tree
        for child in new_kids:
            tree_view.add_node(child, parent_map[child])

        # mark visited on the grid (preserves START / GOAL colours)
        if node and step_type == 'step':
            grid.mark_visited(*node)

        # agent perception: current cell + traversable cardinal neighbours
        _, perceived = agent.perceive(node) if node else (None, [])
        perception = ([node] + perceived) if node else None

        # redraw both panels
        grid_view.draw(grid, current_agent=node, perception=perception)
        tree_view.draw(current=node, frontier=frontier)
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(delay)

        if step_type in ('found', 'no_path'):
            final_state = state
            break

    plt.ioff()

    # ------------------------------------------------------------------ #
    # 5. Final frame — highlight the path (or report no solution)
    # ------------------------------------------------------------------ #
    if final_state and final_state['type'] == 'found':
        path = final_state['path']
        print(f"Path found!  Length : {len(path) - 1} step(s)")
        print(f"States searched     : {agent.states_searched}")

        # mark path on the grid model
        for r, c in path:
            grid.mark_path(r, c)

        grid_view.draw(grid, current_agent=grid.goal)
        tree_view.draw(current=grid.goal, path=path)

        ax_grid.set_title(
            f"2D Grid — {method.upper()} | Path length: {len(path)-1}",
            fontsize=11, fontweight="bold",
        )
        ax_tree.set_title(
            f"Search Tree — {agent.states_searched} states explored",
            fontsize=11, fontweight="bold",
        )

    else:
        print("No path found.")
        print(f"States searched : {agent.states_searched}")

        grid_view.draw(grid)
        tree_view.draw()

        ax_grid.set_title(
            f"2D Grid — {method.upper()} | No path exists",
            fontsize=11, fontweight="bold",
        )
        ax_tree.set_title(
            f"Search Tree — {agent.states_searched} states explored",
            fontsize=11, fontweight="bold",
        )

    plt.tight_layout(pad=2.5)
    plt.show(block=True)


# ------------------------------------------------------------------ #
# CLI
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Uninformed search on a 2-D grid (BFS / DFS)"
    )
    parser.add_argument("--size",    type=int,   default=10,
                        help="Grid size NxN (default: 10)")
    parser.add_argument("--density", type=float, default=0.25,
                        help="Obstacle density 0–1 (default: 0.25)")
    parser.add_argument("--method",  choices=['bfs', 'dfs'], default='bfs',
                        help="Search method: bfs or dfs (default: bfs)")
    parser.add_argument("--delay",   type=float, default=0.15,
                        help="Animation delay in seconds (default: 0.15)")
    args = parser.parse_args()

    main(size=args.size, density=args.density,
         method=args.method, delay=args.delay)
