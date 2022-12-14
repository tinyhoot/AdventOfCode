import re

from utils.puzzles.geometry import DictGrid, Line, Point
from utils.solution import BaseSolution


class Solution(BaseSolution):

    def parse(self, raw: str):
        raw = raw.rstrip("\n")
        lines = []
        for group in raw.splitlines():
            points_strs = map(lambda s: s.split(","), re.findall(r"\d+,\d+", group))
            points = [Point(int(point[0]), int(point[1])) for point in points_strs]
            idx = 1
            while idx < len(points):
                lines.append(Line(points[idx-1], points[idx]))
                idx += 1

        return lines

    def part1(self, data):
        """How many grains of sand come to rest before they start falling off into infinity?"""
        grid = DictGrid()
        for line in data:
            grid.add_line(line)
        lowest_point = max(grid._grid.keys(), key=lambda p: p[1])

        # Set up sand and the directions it can fall in.
        sand_origin = Point(500, 0)
        sand = sand_origin.copy()
        down, down_left, down_right = Point(0, 1), Point(-1, 1), Point(1, 1)
        while sand.y < lowest_point[1] + 1:
            if not grid.get(sand + down):
                sand.move(delta=down)
            elif not grid.get(sand + down_left):
                sand.move(delta=down_left)
            elif not grid.get(sand + down_right):
                sand.move(delta=down_right)
            else:
                # If the sand cannot move anywhere else, it settles.
                grid.add_point(sand, 5)
                # print(f"Settled at {sand}")
                sand = sand_origin.copy()

        # Return the number of sand kernels in the grid.
        return len([s for s in filter(lambda x: x[1] == 5, grid._grid.items())])

    def part2(self, data):
        """How many grains of sand come to rest before they block off the origin?"""
        grid = DictGrid()
        for line in data:
            grid.add_line(line)
        lowest_point = max(grid._grid.keys(), key=lambda p: p[1])

        # Set up sand and the directions it can fall in.
        sand_origin = Point(500, 0)
        sand = sand_origin.copy()
        down, down_left, down_right = Point(0, 1), Point(-1, 1), Point(1, 1)
        while grid.get(sand_origin) is None:
            # Assume an infinite floor at lowest+2
            if sand.y == lowest_point[1] + 1:
                grid.add_point(sand, 5)
                sand = sand_origin.copy()
            # Proceed as before.
            if not grid.get(sand + down):
                sand.move(delta=down)
            elif not grid.get(sand + down_left):
                sand.move(delta=down_left)
            elif not grid.get(sand + down_right):
                sand.move(delta=down_right)
            else:
                # If the sand cannot move anywhere else, it settles.
                grid.add_point(sand, 5)
                # print(f"Settled at {sand}")
                sand = sand_origin.copy()

        # Return the number of sand kernels in the grid.
        return len([s for s in filter(lambda x: x[1] == 5, grid._grid.items())])


if __name__ == "__main__":
    solution = Solution()
    solution.solve(True)
