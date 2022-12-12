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
        """What is the fewest steps required to move from your current position to the end?"""
        print(data.pretty_print())
        print("---")
        start = data.index(0)
        end = data.index(27)
        print(f"Start: {start}\tEnd: {end}")
        self.nodes = data
        path = dijkstra(data, start, end, self._get_distance)

        return path

    def part2(self, data):
        pass


if __name__ == "__main__":
    solution = Solution()
    solution.solve(True)
