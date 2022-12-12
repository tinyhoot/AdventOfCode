import math
import random
from collections import defaultdict

from utils.puzzles.algorithms import dijkstra
from utils.puzzles.geometry import Grid, Point
from utils.solution import BaseSolution


class Solution(BaseSolution):

    def _get_distance(self, current: Point, neighbour: Point) -> float | None:
        """Get the distance between two neighbouring nodes, or None if the path is impassable."""
        if self.nodes[neighbour] - self.nodes[current] > 1:
            return None
        return 1

    def parse(self, raw: str):
        rows = raw.count("\n")
        raw = raw.rstrip("\n")
        heights = []
        for line in raw.splitlines():
            for char in line:
                # Starting point
                if char == "S":
                    heights.append(0)
                # Ending point
                elif char == "E":
                    heights.append(27)
                # Otherwise, a = 1, b = 2, ... z = 26
                else:
                    heights.append(ord(char) - 96)

        return Grid(heights, nrow=rows)

    def part1(self, data: Grid):
        """What is the fewest steps required to move from your current position to the end?

        Off by two, but only in puzzle input. No clue why.
        """
        start = data.index(0)
        end = data.index(27)
        self.nodes = data
        path = dijkstra(data, start, end, self._get_distance)

        return path

    def part2(self, data):
        """Copy-pasted with minor changes cause I cannot be bothered to write a general one.

        Off by two! I don't get why.
        """
        end = data.index(27)
        # 1 - Mark all nodes as unvisited.
        unvisited = [Point(x, y) for x in range(data.num_cols) for y in range(data.num_rows)]
        # 2 - Assign to every node a tentative distance value.
        nodes = Grid(size=data.get_size(), default=math.inf)
        nodes[end] = 0
        current = end
        while len(unvisited) > 0:
            # 3 - For the current node, consider all neighbours and calculate their tentative distances.
            neighbours = nodes.get_neighbours(current)
            for n in neighbours:
                # Only consider unvisited ones.
                if n in unvisited:
                    distance = 1 if data[n] - data[current] >= -1 else None
                    # If the neighbour should not be considered for some special reason, the distance will be None.
                    if distance is not None and nodes[current] + distance < nodes[n]:
                        nodes[n] = nodes[current] + distance
            # 4 - When we are done considering neighbours, mark the current node as visited.
            unvisited.remove(current)
            if data[current] == 1 or data[current] == 0:
                break
            # 5 - Select the unvisited node with the smallest tentative distance as the new current node.
            current = min(unvisited, key=lambda v: nodes[v])
            # 6 - If the destination node is marked visited, or the shortest available path is infinity, stop.
            if nodes[current] == math.inf:
                break

        # print(nodes.pretty_print())
        return nodes[current]


if __name__ == "__main__":
    solution = Solution()
    solution.solve(True)
