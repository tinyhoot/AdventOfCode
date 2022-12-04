import re

from utils.puzzles.numbers import IntRange
from utils.solution import Solution


class Day04Solution(Solution):

    def parse(self, raw: str):
        raw = raw.rstrip("\n")
        cleaning = []
        for line in raw.split("\n"):
            numbers = tuple(map(int, re.split("[,-]", line)))
            duties = [IntRange(numbers[idx], numbers[idx+1]) for idx in range(len(numbers)) if idx % 2 == 0]
            cleaning.append(duties)

        return cleaning

    def part1(self, data) -> int:
        """How many elves' cleaning duties completely contain each other?"""
        print(data)
        total = 0
        for pair in data:
            if pair[0] in pair[1] or pair[1] in pair[0]:
                total += 1

        return total

    def part2(self, data) -> int:
        total = 0
        for pair in data:
            if pair[0].overlaps(pair[1]):
                total += 1

        return total


if __name__ == "__main__":
    solution = Day04Solution()
    solution.solve(False)
