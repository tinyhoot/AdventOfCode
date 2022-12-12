from collections import defaultdict

from utils.puzzles.geometry import Grid
from utils.solution import BaseSolution


class Solution(BaseSolution):

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
        step_size = 1
        print(f"Start: {start}\tEnd: {end}")
        path = Grid(size=data.get_size(), default=-1)
        path[start] = 0

        # Approach: Assemble a list of which locations to explore next.
        process_path = {start}
        while len(process_path) > 0:
            idx = process_path.pop()
            print(f"Exploring {idx}")
            neighbours = data.get_neighbours(idx)
            for n in neighbours:
                if abs(data[idx] - data[n]) <= step_size:
                    # This neighbour is in range. Has it already been explored?
                    if path[n] != -1 and (path[idx] == -1 or path[n] < path[idx]):
                        # It has been explored and may be a shorter path to the current place.
                        path[idx] = path[n] + 1
                    else:
                        # (Re-)explore this neighbour.
                        process_path.add(n)
            #print(path.pretty_print())
            #print("---")
            if idx == end:
                break
        print(path.pretty_print())
        return path[end]

    def part2(self, data):
        pass


if __name__ == "__main__":
    solution = Solution()
    solution.solve(True)
