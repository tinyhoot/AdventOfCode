from utils.puzzles.geometry import Point
from utils.solution import BaseSolution


class Solution(BaseSolution):

    directions_nswe = (0, -1), (0, 1), (-1, 0), (1, 0)

    def _get_to_edge(self, data, pos: Point, delta):
        """Get all elements from the given position to one of the edges of the forest."""
        pos = pos + delta
        while 0 <= pos.y < len(data) and 0 <= pos.x < len(data[pos.y]):
            yield data[pos.y][pos.x]
            pos = pos + delta

    def parse(self, raw: str):
        raw = raw.rstrip("\n")
        return [[int(tree) for tree in line] for line in raw.split("\n")]

    def part1(self, data) -> int:
        """How many trees are visible from outside the grid?"""
        total = 0
        for y, line in enumerate(data):
            for x, tree in enumerate(line):
                # Look in each of the cardinal directions.
                for direction in self.directions_nswe:
                    visible = True
                    for neighbour in self._get_to_edge(data, Point(x, y), direction):
                        if neighbour >= tree:
                            visible = False
                            break
                    if visible:
                        total += 1
                        break

        return total

    def part2(self, data):
        """What is the best scenic score possible, i.e. how many trees can you possibly see at once from inside?"""
        best_score = 0
        for y, line in enumerate(data):
            for x, tree in enumerate(line):
                score = 1
                # Look in each of the cardinal directions.
                for direction in self.directions_nswe:
                    visible = 0
                    # This will actually zero out on trees at the edge of the forest, but I got lucky
                    # and it worked anyway.
                    for neighbour in self._get_to_edge(data, Point(x, y), direction):
                        visible += 1
                        if neighbour >= tree:
                            break
                    score *= visible
                if score > best_score:
                    best_score = score

        return best_score


if __name__ == "__main__":
    solution = Solution()
    solution.solve(False)
