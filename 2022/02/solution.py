from utils.solution import Solution


class Day02Solution(Solution):

    def parse(self, raw: str) -> list[list[str]]:
        raw = raw.rstrip("\n")
        strategy = []
        for line in raw.split("\n"):
            strategy.append(line.split())
        return strategy

    def part1(self, data) -> int:
        """How high would your score be if you interpreted 'XYZ' as Rock, Paper, Scissors?"""
        score = 0
        for line in data:
            # Convert XYZ to valid ABC moves.
            moves = {"X": "A", "Y": "B", "Z": "C"}
            player = line[1].translate(str.maketrans(moves))
            score += self._rps(line[0], player)
        return score

    def part2(self, data) -> int:
        """How high would your score be if you interpreted 'XYZ' as Losing, Draw, Winning?"""
        score = 0
        for line in data:
            rules = "ABCAB"
            # Because XYZ means losing, draw, or winning, we can interpret this as an index shift,
            # where X means -1, Y is 0, and Z is 1.
            outcome = "XYZ".find(line[1]) - 1
            elf_move = rules.find(line[0], 1)
            p_move = rules[elf_move + outcome]
            score += self._rps(line[0], p_move)
        return score

    def _rps(self, elf: str, player: str) -> int:
        """Get the score for a game of rock paper scissors."""
        rps_rules = "ABCAB"
        score = ord(player) - 64
        player_idx = rps_rules.find(player, 1)
        elf_idx = rps_rules.find(elf, player_idx - 1)
        if player_idx < elf_idx:
            return 0 + score
        if player_idx == elf_idx:
            return 3 + score
        if player_idx > elf_idx:
            return 6 + score


if __name__ == "__main__":
    solution = Day02Solution()
    solution.solve(False)
