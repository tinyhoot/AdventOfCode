from collections import namedtuple

from utils.solution import BaseSolution


class Solution(BaseSolution):

    def parse(self, raw: str):
        raw = raw.rstrip("\n")
        root = Directory("/")
        current_dir = root
        for line in raw.split("\n"):
            if line.startswith("$"):
                # Execute a command.
                cmd = line.split()
                if cmd[1] == "ls":
                    continue
                if cmd[1] == "cd":
                    if cmd[2] == "/":
                        current_dir = root
                    elif cmd[2] == "..":
                        current_dir = current_dir.parent
                    else:
                        current_dir = current_dir.find_dir(cmd[2])
            else:
                # Add some files to the current directory.
                self._parse_child(line, current_dir)

        return root

    def _parse_child(self, line: str, current_dir: "Directory"):
        line_split = line.split()
        # If the parse succeeds, it is a file. Otherwise, it is a directory.
        try:
            size = int(line_split[0])
            current_dir.create_file(line_split[1], size)
        except ValueError:
            current_dir.mkdir(line_split[1])

    def part1(self, data: "Directory") -> int:
        """Find the total size of all folders which are less than 100000 in size."""
        return sum(map(lambda d: d.size, filter(lambda d: d.size <= 100000, data.get_all_dirs())))

    def part2(self, data: "Directory") -> int:
        """Find the smallest directory that, if deleted, would free up enough space to pass 30000000 in free space."""
        used = data.size
        space_needed = used - 40000000
        return min(map(lambda d: d.size, filter(lambda d: d.size >= space_needed, data.get_all_dirs())))


class Directory:

    File = namedtuple("File", ["name", "size"])

    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.contents = []

    def __repr__(self):
        return f"<Directory {self.name}>"

    def __str__(self):
        return self.name + "\n" + "\n".join(self._pretty_print())

    def create_file(self, name: str, size: int):
        """Create a new file in this directory."""
        self.contents.append(self.File(name, size))

    def find_dir(self, name: str) -> "Directory":
        """Try to find a specific child directory."""
        for child in self.contents:
            if isinstance(child, type(self)) and child.name == name:
                return child
        raise ValueError(f"No directory of name '{name}' exists in {self.name}!")

    def get_all_dirs(self):
        """Yields this directory along with all child directories."""
        yield self
        for child in self.contents:
            if isinstance(child, type(self)):
                yield from child.get_all_dirs()

    def mkdir(self, name: str) -> "Directory":
        """Creates a new child directory inside this one."""
        new_dir = Directory(name, self)
        self.contents.append(new_dir)
        return new_dir

    def _pretty_print(self):
        for child in self.contents:
            if isinstance(child, type(self)):
                yield "|-- DIR " + child.name
                for child_child in child._pretty_print():
                    yield "    " + child_child
            else:
                yield "|-- " + child.name

    @property
    def size(self) -> int:
        """Get the total size of all files and subdirectories in this directory."""
        return sum(map(lambda x: x.size, self.contents))


if __name__ == "__main__":
    solution = Solution()
    solution.solve(False)
