from utils.solution import Solution


class Day01Solution(Solution):

    TEST_DATA = "1000\n2000\n3000\n\n4000\n\n5000\n6000\n\n7000\n8000\n9000\n\n10000"

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
    solution.solve(2, False)
