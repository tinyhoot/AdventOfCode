# Things that help with solving puzzles that relate to numbers in some way.
from collections.abc import Sequence
from math import sqrt


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

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __sub__(self, other):
        if isinstance(other, type(self)):
            return Point(self.x - other.x, self.y - other.y)
        if isinstance(other, Sequence) and len(other) == 2:
            return Point(self.x - other[0], self.y - other[1])
        raise ValueError

    def distance(self, point: "Point") -> float:
        x = (self.x - point.x)**2
        y = (self.y - point.y)**2
        return sqrt(x + y)

    def move(self, x=None, y=None, delta=None):
        if x is not None or y is not None:
            self.x += x if x is not None else 0
            self.y += y if y is not None else 0
            return
        if isinstance(delta, type(self)):
            self.x += delta.x
            self.y += delta.y
            return
        if isinstance(delta, Sequence) and len(delta) == 2:
            self.x += delta[0]
            self.y += delta[1]
            return
        raise ValueError

    def normalise(self, max: int = 1):
        """Return a new point with this point's positions capped at 1."""
        if self.x != 0:
            x = self.x // abs(self.x) * max
        else:
            x = 0
        if self.y != 0:
            y = self.y // abs(self.y) * max
        else:
            y = 0
        return Point(x, y)

    def to_tuple(self) -> tuple[int, int]:
        return self.x, self.y
