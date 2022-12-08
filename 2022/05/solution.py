import copy
import re

from utils.solution import BaseSolution


class Solution(BaseSolution):

    def _get_result(self, crates: list[list]) -> str:
        result = ""
        for stack in crates:
            if len(stack) > 0:
                result += stack[-1]

        return result

    def _move_crate(self, crates: list[list], target: int, destination: int):
        crate = crates[target].pop()
        crates[destination].append(crate)

    def parse(self, raw: str):
        raw = raw.rstrip("\n")
        # The last number in the line before instructions start must signify the number of crate stacks.
        num_cols = int(re.search(r"\d+\s*\n\n", raw)[0])
        crates = [[] for _ in range(num_cols)]
        crates_raw, moves_raw = raw.split("\n\n")

        for line in crates_raw.split("\n"):
            # The crate names, if they exist, show up at set intervals.
            for idx in range(1, len(line), 4):
                if line[idx].isalpha():
                    stack = idx // 4
                    crates[stack].insert(0, line[idx])

        moves = []
        for line in moves_raw.split("\n"):
            moves.append(tuple(map(int, re.findall(r"\d+", line))))

        return crates, moves

    def part1(self, data) -> str:
        """What do the final stacks look like if moving crates one at a time?"""
        crates, moves = data
        crates = copy.deepcopy(crates)
        for move in moves:
            # Move the crates one by one.
            for _ in range(move[0]):
                self._move_crate(crates, move[1] - 1, move[2] - 1)

        return self._get_result(crates)

    def part2(self, data):
        """What do the final stacks look like if moving crates all at once?"""
        crates, moves = data
        for move in moves:
            num, target, destination = move[0], move[1] - 1, move[2] - 1
            payload = crates[target][-num:]
            crates[target] = crates[target][:-num]
            crates[destination] = crates[destination] + payload

        return self._get_result(crates)


if __name__ == "__main__":
    solution = Solution()
    solution.solve(False)
