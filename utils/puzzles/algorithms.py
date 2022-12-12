import math
from typing import Callable

from utils.puzzles.geometry import Grid, Point


def dijkstra(grid: Grid, start: Point, end: Point, distance_func: Callable[[Point, Point], float | None]) -> float:
    """Find the shortest path from start to end."""
    # 1 - Mark all nodes as unvisited.
    unvisited = [Point(x, y) for x in range(grid.num_cols) for y in range(grid.num_rows)]
    # 2 - Assign to every node a tentative distance value.
    nodes = Grid(size=grid.get_size(), default=math.inf)
    nodes[start] = 0
    current = start
    while len(unvisited) > 0:
        # 3 - For the current node, consider all neighbours and calculate their tentative distances.
        neighbours = nodes.get_neighbours(current)
        for n in neighbours:
            # Only consider unvisited ones.
            if n in unvisited:
                distance = distance_func(current, n)
                # If the neighbour should not be considered for some special reason, the distance will be None.
                if distance is not None and nodes[current] + distance < nodes[n]:
                    nodes[n] = nodes[current] + distance
        # 4 - When we are done considering neighbours, mark the current node as visited.
        unvisited.remove(current)
        if current == end:
            break
        # 5 - Select the unvisited node with the smallest tentative distance as the new current node.
        current = min(unvisited, key=lambda v: nodes[v])
        # 6 - If the destination node is marked visited, or the shortest available path is infinity, stop.
        if nodes[current] == math.inf:
            break

    # print(nodes.pretty_print())
    return nodes[end]
