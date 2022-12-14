from utils.puzzles.numbers import Point
from utils.solution import BaseSolution


class Solution(BaseSolution):

    MOVES = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0)
    }

    def _catchup(self, head: Point, tail: Point):
        """Move the tail to catch up with the head."""
        diff = head - tail
        x = abs(diff.x)
        y = abs(diff.y)
        if (x > 1 and y <= 1) or (x <= 1 and y > 1):
            tail.move(delta=diff.signage())
        if x > 1 and y > 1:
            tail.move(delta=diff.signage())

    def parse(self, raw: str):
        raw = raw.rstrip("\n")
        steps = []
        for line in raw.split("\n"):
            direction, num = line.split()
            steps.append((direction, int(num)))

        return steps

    def part1(self, data):
        """How many positions does the tail of the rope visit at least once?"""
        head = Point(0, 0)
        tail = Point(0, 0)
        positions = set()
        for step in data:
            # Do every step one increment at a time.
            for _ in range(step[1]):
                delta = self.MOVES[step[0]]
                head.move(delta=delta)
                self._catchup(head, tail)
                positions.add(tail.to_tuple())

        return len(positions)

    def part2(self, data):
        """How many positions does the tail of the rope visit at least once?"""
        head = Point(0, 0)
        tail = [Point(0, 0) for _ in range(9)]
        positions = set()
        for step in data:
            # Do every step one increment at a time.
            for _ in range(step[1]):
                delta = self.MOVES[step[0]]
                head.move(delta=delta)
                # Now catch up the other nine segments.
                self._catchup(head, tail[0])
                for idx in range(1, 9):
                    self._catchup(tail[idx-1], tail[idx])
                positions.add(tail[-1].to_tuple())

        return len(positions)


if __name__ == "__main__":
    solution = Solution()
    solution.solve(True)
