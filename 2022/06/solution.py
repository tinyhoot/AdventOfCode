from utils.solution import BaseSolution


class Solution(BaseSolution):

    def parse(self, raw: str):
        raw = raw.rstrip("\n")
        return raw

    def part1(self, data) -> int:
        """At which index do we have four different letters for the first time?"""
        for idx in range(4, len(data)):
            if len(set(data[idx-4:idx])) == 4:
                return idx

    def part2(self, data) -> int:
        """At which index do we have fourteen different letters for the first time?"""
        for idx in range(14, len(data)):
            if len(set(data[idx-14:idx])) == 14:
                return idx


if __name__ == "__main__":
    solution = Solution()
    solution.solve(False)
