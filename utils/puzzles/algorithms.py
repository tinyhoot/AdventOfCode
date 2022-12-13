import math
from typing import Any, Callable

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


def _merge(left: list, right: list, comp_func: Callable[[Any, Any], bool]) -> list:
    if len(left) == 0:
        return right
    if len(right) == 0:
        return left

    result = []
    idx_l = idx_r = 0
    # Iterate through both arrays until all elements are in the result.
    while len(result) < len(left) + len(right):
        # Choose the "smaller" element.
        if comp_func(left[idx_l], right[idx_r]):
            result.append(left[idx_l])
            idx_l += 1
        else:
            result.append(right[idx_r])
            idx_r += 1
        # If the end of either array is reached, append the rest of the other.
        if idx_l == len(left):
            result += right[idx_r:]
            break
        if idx_r == len(right):
            result += left[idx_l:]
            break

    return result


def merge_sort(array: list, comparison_func: Callable[[Any, Any], bool]) -> list:
    """Sort the given array using the MergeSort algorithm."""
    if len(array) < 2:
        return array
    middle = len(array) // 2
    # Sort the array by recursively splitting it in half, sorting those halves, and then merging them back together.
    return _merge(merge_sort(array[:middle], comparison_func), merge_sort(array[middle:], comparison_func), comparison_func)
