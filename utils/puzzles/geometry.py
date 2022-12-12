# Classes which help with modeling geometry.
from typing import Sequence


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
        if isinstance(item, Sequence) and len(item) == 2:
            return self._values[item[0] * self.num_cols + item[1]]
        raise TypeError

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._values[key] = value
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

    def get_neighbours(self, index):
        """Get all neighbouring elements of the element at the given grid index in clockwise order."""
        if not isinstance(index, Sequence) or len(index) != 2:
            raise AttributeError("Index must be a tuple of size 2.")
        row, col = index
        neighbours = []
        if row > 0:
            neighbours.append((row-1, col))
        if col < self.num_cols - 1:
            neighbours.append((row, col+1))
        if row < self.num_rows - 1:
            neighbours.append((row+1, col))
        if col > 0:
            neighbours.append((row, col-1))
        return neighbours


    def get_size(self) -> tuple[int, int]:
        """Get the number of rows and columns in the grid."""
        return self.num_rows, self.num_cols

    def index(self, item) -> tuple[int, int]:
        """Find the position of the given item."""
        idx = self._values.index(item)
        return self._to_grid_idx(idx)

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

    def _to_grid_idx(self, index) -> tuple[int, int]:
        """Convert a values list index to its index in the grid."""
        return index // self.num_cols, index % self.num_cols

    def values(self):
        """Yield all values in the grid in one flat list."""
        yield from self._values

