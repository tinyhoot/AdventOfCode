import re

from utils.solution import BaseSolution


class Solution(BaseSolution):

    def parse(self, raw: str):
        raw = raw.rstrip("\n")
        monkeys = []
        for section in raw.split("\n\n"):
            section = section.split("\n")
            monkey_id = int(re.search(r"\d+", section[0])[0])
            items = [int(match) for match in re.findall(r"\d+", section[1])]
            operation = re.search(r"new = (.*)", section[2])[1]
            test = int(re.search(r"\d+", section[3])[0])
            throw_true = int(re.search(r"\d+", section[4])[0])
            throw_false = int(re.search(r"\d+", section[5])[0])

            monkey = Monkey(monkey_id, items, operation, test, (throw_true, throw_false))
            monkeys.append(monkey)

        # Just to make sure, sort them.
        monkeys.sort(key=lambda m: m.id)
        return monkeys

    def part1(self, data: list):
        """Find the two most active monkeys over 20 rounds."""
        activity = [0 for _ in range(len(data))]
        for _ in range(20):
            for monkey in data:
                activity[monkey.id] += len(monkey.items)
                monkey.inspect(data)

        activity.sort(reverse=True)
        print(activity)
        return activity[0] * activity[1]

    def part2(self, data):
        """Without decreasing worry levels, what is the level of monkey business after 10000 rounds?"""
        prime_mult = 1
        # No decreasing levels means the numbers escalate out of control. Exploit modular arithmetic instead.
        # Reducing worry sizes by the modulus of all divisors multiplied together yields the same results as the
        # actual, massive numbers.
        for monkey in data:
            prime_mult *= monkey.test_div

        activity = [0 for _ in range(len(data))]
        for round in range(10000):
            print(f"\r=== Round {round+1} ===", end="")
            for monkey in data:
                activity[monkey.id] += len(monkey.items)
                monkey.inspect(data, False, prime_mult)

        activity.sort(reverse=True)
        print("")
        print(activity)
        return activity[0] * activity[1]


class Monkey:

    def __init__(self, id: int, starting_items: list, operation: str, test: int, throw_to: tuple[int, int]):
        self.id = id
        self.items = starting_items
        self.operation = operation
        self.test_div = test
        self.next = throw_to

    def __str__(self):
        return f"Monkey {self.id}, {self.items}"

    def catch(self, item):
        """Catch an item passed to this monkey by another monkey."""
        self.items.append(item)

    def inspect(self, monkeys: list["Monkey"], decrease_worry: bool = True, prime_mult: int = 0):
        """Inspect an item and perform the specified operations on it."""
        while len(self.items) > 0:
            item = self.items.pop(0)
            # Prepare variable for the eval operation.
            old = item
            item = eval(self.operation)
            # Part 1 vs Part 2.
            if decrease_worry:
                item = item // 3
            else:
                # Reduce by the product of the divisors of all monkeys.
                item %= prime_mult
            self.throw(item, monkeys)

    def test(self, item) -> bool:
        return item % self.test_div == 0

    def throw(self, item, monkeys: list["Monkey"]):
        """Throw the item to a different monkey based on a testing criterium."""
        if self.test(item):
            monkeys[self.next[0]].catch(item)
        else:
            monkeys[self.next[1]].catch(item)


if __name__ == "__main__":
    solution = Solution()
    solution.solve(True)
