# Things that help with solving puzzles that relate to numbers in some way.
from collections.abc import Sequence


class IntRange:
    """An inclusive range of numbers with a defined start and end."""

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"<{self.__str__()}>"

    def __str__(self):
        return f"{self.start}-{self.end}"

    def __contains__(self, item):
        if isinstance(item, IntRange):
            return self.start <= item.start and self.end >= item.end
        if isinstance(item, int) or isinstance(item, float):
            return self.start <= item <= self.end
        return False

    def iter(self):
        """Iterate over each number from start to end, inclusive."""
        for x in range(self.start, self.end + 1):
            yield x

    def overlaps(self, other: "IntRange") -> bool:
        """Check whether this range overlaps another one."""
        return (other.start <= self.start <= other.end) or (other.start <= self.end <= other.end) or other in self


class Point:
    """A point in a coordinate system."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, type(self)):
            return Point(self.x + other.x, self.y + other.y)
        if isinstance(other, Sequence) and len(other) == 2:
            return Point(self.x + other[0], self.y + other[1])
        raise ValueError
