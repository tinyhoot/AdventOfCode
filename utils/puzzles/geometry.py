# Classes which help with modeling geometry.
from math import sqrt
from typing import Any, Sequence


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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __sub__(self, other):
        if isinstance(other, type(self)):
            return Point(self.x - other.x, self.y - other.y)
        if isinstance(other, Sequence) and len(other) == 2:
            return Point(self.x - other[0], self.y - other[1])
        raise TypeError

    def copy(self) -> "Point":
        return Point(self.x, self.y)

    def distance(self, other: "Point") -> float:
        x = (self.x - other.x) ** 2
        y = (self.y - other.y) ** 2
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
        raise TypeError

    def signage(self, max: int = 1):
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


class Line:
    """A line in a coordinate system."""

    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b

    def __iter__(self):
        """Yield all points along the line."""
        step = (self.b - self.a).signage()
        current = self.a
        yield self.a
        while current != self.b:
            current += step
            yield current

    def __len__(self):
        return self.a.distance(self.b)

    def __str__(self):
        return f"({self.a.x},{self.a.y} -> {self.b.x},{self.b.y})"


class Grid:

    def __init__(self, values: list = None, ncol: int = None, nrow: int = None, size: tuple[int, int] = None,
                 default=0):
        # "values" here expects data to come in row by row, column by column.
        if values:
            if ncol is not None:
                self.num_cols = ncol
                self.num_rows = len(values) // ncol
            elif nrow is not None:
                self.num_rows = nrow
                self.num_cols = len(values) // nrow
            else:
                raise AttributeError("One of 'ncol' or 'nrow' must be given if 'values' was passed!")
            self._values = values
        else:
            if not size:
                raise AttributeError("If 'values' is not defined, 'size' must be passed!")
            self._values = [default for _ in range(size[0] * size[1])]
            self.num_rows, self.num_cols = size

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._values[item]
        if isinstance(item, Point):
            return self._values[item.y * self.num_cols + item.x]
        if isinstance(item, Sequence) and len(item) == 2:
            return self._values[item[0] * self.num_cols + item[1]]
        raise TypeError

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._values[key] = value
        elif isinstance(key, Point):
            self._values[key.y * self.num_cols + key.x] = value
        elif isinstance(key, Sequence) and len(key) == 2:
            self._values[key[0] * self.num_cols + key[1]] = value
        else:
            raise TypeError

    def __str__(self):
        return f"Grid{self.get_size()}"

    def by_col(self):
        """Get all values in the grid, organised by column."""
        for col_idx in range(self.num_cols):
            yield [self._values[col_idx + row_idx * self.num_cols] for row_idx in range(self.num_rows)]

    def by_row(self):
        """Get all values in the grid, organised by row."""
        for row_idx in range(self.num_rows):
            yield [self._values[row_idx * self.num_cols + col_idx] for col_idx in range(self.num_cols)]

    def get_neighbours(self, idx: Point) -> list[Point]:
        """Get all neighbouring elements of the element at the given grid index in clockwise order."""
        neighbours = []
        if idx.y > 0:
            neighbours.append(Point(idx.x, idx.y - 1))
        if idx.x < self.num_cols - 1:
            neighbours.append(Point(idx.x + 1, idx.y))
        if idx.y < self.num_rows - 1:
            neighbours.append(Point(idx.x, idx.y + 1))
        if idx.x > 0:
            neighbours.append(Point(idx.x - 1, idx.y))
        return neighbours

    def get_size(self) -> tuple[int, int]:
        """Get the number of rows and columns in the grid."""
        return self.num_rows, self.num_cols

    def index(self, item) -> Point:
        """Find the position of the given item."""
        idx = self._values.index(item)
        return self._to_point(idx)

    def pretty_print(self) -> str:
        """Get an easily printable version of the grid."""
        output = ""
        # Get the length of the longest string of all values contained within.
        longest = max(map(len, map(str, self.values())))
        for row in self.by_row():
            output += "[ "
            for value in row:
                # Adjust all values to be in neat, equal-sized rows.
                output += f"{value: >{longest}}, "
            output = output.rstrip(", ")
            output += " ]\n"

        output = output.rstrip("\n")
        return output

    def _to_point(self, index) -> Point:
        """Convert a values list index to its index in the grid."""
        return Point(index % self.num_cols, index // self.num_cols)

    def values(self):
        """Yield all values in the grid in one flat list."""
        yield from self._values


class DictGrid:
    """Emulate an infinite coordinate system."""

    def __init__(self):
        self._grid = {}

    def __len__(self):
        return len(self._grid)

    def add_line(self, line: Line):
        """Add a series of points to the grid."""
        for point in line:
            self._grid[point.to_tuple()] = 1

    def add_point(self, point: Point, value: Any = 1):
        """Add a point to the grid."""
        self._grid[point.to_tuple()] = value

    def get(self, point: Point | tuple[int, int]):
        """Gets the value associated with the given point, or None if it does not exist."""
        if isinstance(point, Point):
            point = point.to_tuple()
        return self._grid.get(point, None)

