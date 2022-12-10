from utils.solution import BaseSolution


class Solution(BaseSolution):

    def parse(self, raw: str):
        raw = raw.rstrip("\n")
        instructions = []
        for line in raw.splitlines():
            cmd = line.split()
            if len(cmd) > 1:
                cmd[1] = int(cmd[1])
            instructions.append(cmd)

        return instructions

    def part1(self, data):
        """
        Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles.
        What is the sum of these six signal strengths?
        """
        key_cycles = [20, 60, 100, 140, 180, 220]
        cpu = CPU(data)
        signals = [signal for signal in cpu.process(key_cycles[:])]
        signal_strengths = sum(map(lambda x: x[0]*x[1], zip(key_cycles, signals)))
        return signal_strengths

    def part2(self, data):
        """Render the image given by your program. What eight capital letters appear on your CRT?"""
        cpu = CPU(data)
        cpu.process_crt()
        for line in cpu.screen:
            print(line)


class CPU:

    def __init__(self, instructions: list):
        self.instructions = instructions

        self.cycle = 0
        self.registerX = 1
        self.screen = []

    def draw(self):
        """Draw one pixel on the screen for the current cycle."""
        draw_pos = (self.cycle-1) % 40
        if draw_pos == 0:
            self.screen.append("")
        if abs(self.registerX - draw_pos) <= 1:
            pixel = "#"
        else:
            pixel = "."
        print(f"Drawing pixel in pos {draw_pos}: {pixel}, X at {self.registerX}")
        self.screen[-1] = self.screen[-1] + pixel

    def process(self, key_cycles: list):
        """Process all instructions and yield data at specific cycles."""
        for cmd in self.instructions:
            x_during = self.registerX
            if cmd[0] == "noop":
                self.cycle += 1
                continue
            # Only other option is the 'addx' instruction.
            self.cycle += 2
            self.registerX += cmd[1]
            # If a key cycle was reached, yield the register during this cycle.
            if len(key_cycles) > 0 and self.cycle >= key_cycles[0]:
                key_cycles.pop(0)
                yield x_during

    def process_crt(self):
        """Process all instructions and draw to CRT at each cycle."""
        instruction_idx = -1
        cycles_to_finish = 1
        while instruction_idx < len(self.instructions) - 1:
            self.cycle += 1
            cycles_to_finish -= 1
            if cycles_to_finish == 0:
                # Finish processing the current instruction and advance to the next one.
                if self.instructions[instruction_idx][0] == "addx":
                    self.registerX += self.instructions[instruction_idx][1]
                instruction_idx += 1
                if self.instructions[instruction_idx][0] == "noop":
                    cycles_to_finish = 1
                else:
                    cycles_to_finish = 2
            # Draw a pixel to CRT.
            self.draw()


if __name__ == "__main__":
    solution = Solution()
    solution.solve(True)
