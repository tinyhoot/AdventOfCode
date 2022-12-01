from utils.solution import Solution


class Day01Solution(Solution):

    def parse(self, raw: str) -> list[list[int]]:
        elves = []
        for elf in raw.rstrip("\n").split("\n\n"):
            inventory = []
            for food in elf.split("\n"):
                inventory.append(int(food))
            elves.append(inventory)
        return elves

    def part1(self, data) -> int:
        """Find the elf with the highest number of calories in his inventory. How many does he carry?"""
        total_cals = map(sum, data)
        return max(total_cals)

    def part2(self, data) -> int:
        """Find the three elves with the highest number of calories. How many do they carry?"""
        total_cals = sorted(map(sum, data), reverse=True)
        return sum(total_cals[:3])


if __name__ == "__main__":
    solution = Day01Solution()
    solution.solve(False)
