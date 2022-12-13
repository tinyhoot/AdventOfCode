from utils.puzzles.algorithms import merge_sort
from utils.solution import BaseSolution


class Solution(BaseSolution):

    def _compare(self, left_packet: list, right_packet: list) -> bool:
        """Compare two packets against each other. Returns true if they are in the right order."""
        idx = -1
        while idx <= len(left_packet):
            idx += 1
            if idx >= len(left_packet) and idx >= len(right_packet):
                # We should only be reaching the end of both lists as part of an inconclusive sublist.
                return None
            if idx >= len(left_packet):
                return True
            if idx >= len(right_packet):
                return False

            left = left_packet[idx]
            right = right_packet[idx]
            if isinstance(left, int) and isinstance(right, int):
                # Direct comparison is possible.
                if left < right:
                    return True
                if left > right:
                    return False
                continue

            if isinstance(left, int):
                left = [left]
            if isinstance(right, int):
                right = [right]
            # Recurse into comparing sublists.
            result = self._compare(left, right)
            if result is not None:
                return result

        raise RuntimeError

    def parse(self, raw: str):
        raw = raw.rstrip("\n")
        packets = []
        # Split the data into packets with a left and right half.
        for packet in raw.split("\n\n"):
            values = packet.split("\n")
            left = eval(values[0])
            right = eval(values[1])
            packets.append((left, right))

        return packets

    def part1(self, data):
        """What is the sum of the indices of the pairs which are in the right order?"""
        correct = 0
        for idx, packets in enumerate(data):
            left, right = packets
            if self._compare(left, right):
                # Packets are 1-indexed.
                correct += idx + 1

        return correct

    def part2(self, data):
        """Organize all of the packets into the correct order."""
        # For this part, the data should not be organised into left and right halves.
        data_flat = []
        for t in data:
            data_flat.append(t[0])
            data_flat.append(t[1])
        # Add divider packets.
        data_flat.append([[2]])
        data_flat.append([[6]])

        # Sort the packets and find the indices of the divider packets.
        sorted_packets = merge_sort(data_flat, self._compare)
        div_1 = sorted_packets.index([[2]]) + 1
        div_2 = sorted_packets.index([[6]]) + 1

        return div_1 * div_2


if __name__ == "__main__":
    solution = Solution()
    solution.solve(True)
