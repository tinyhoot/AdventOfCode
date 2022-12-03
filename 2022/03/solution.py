from utils.solution import Solution


class DayXXSolution(Solution):

    def _char_to_num(self, char: str) -> int:
        if char.islower():
            return ord(char) - 96
        else:
            return ord(char) - 38

    def parse(self, raw: str):
        raw = raw.rstrip("\n")
        rucksacks = [line for line in raw.split("\n")]
        return rucksacks

    def part1(self, data):
        """Find the duplicate element in each rucksack."""
        total = 0
        for rucksack in data:
            half = len(rucksack) // 2
            comp1 = set(rucksack[:half])
            comp2 = set(rucksack[half:])
            # Use set intersection to find the common element.
            duplicate = comp1 & comp2
            total += self._char_to_num(duplicate.pop())

        return total

    def part2(self, data):
        """Find the common element in every three rucksacks."""
        total = 0
        # Iterate in steps of three, get a whole group at once.
        for idx in range(0, len(data), 3):
            dupe = set(data[idx]) & set(data[idx+1]) & set(data[idx+2])
            total += self._char_to_num(dupe.pop())

        return total


if __name__ == "__main__":
    solution = DayXXSolution()
    solution.solve(False)
