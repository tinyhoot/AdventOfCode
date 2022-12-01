# A base class for solutions during Advent of Code.
import inspect
import logging
import os
from abc import ABCMeta, abstractmethod
from pathlib import Path

from utils import constants, filehandler


class Solution(metaclass=ABCMeta):

    TEST_DATA = None

    def __init__(self):
        self._log = logging.getLogger(constants.ROOT_LOGGER)
        self._log.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("{levelname}:{name}:{message}", style="{"))
        self._log.addHandler(handler)

    def _get_data(self, test_data: bool = True) -> str:
        if test_data:
            if "TEST_DATA" in dir(self) and self.TEST_DATA:
                return self.TEST_DATA
            else:
                raise AttributeError(f"No testing data was defined!")
        else:
            year, day = self._get_day()
            return filehandler.get_puzzle_input(year, day)

    def _get_day(self) -> (int, int):
        """Get the correct year and day based on the filepath of the executing subclass."""
        baseclass = inspect.getframeinfo(inspect.currentframe())
        subclass = None
        # Logically, the first caller with a different filename must be the calling subclass.
        for caller in inspect.getouterframes(inspect.currentframe()):
            if caller.filename != baseclass.filename:
                subclass = caller
                break
        # Failsafe just to be sure we don't do any dumb stuff.
        if not subclass or "AdventOfCode" not in subclass.filename:
            raise FileNotFoundError("Failed to find the calling subclass!")

        subclass_file = Path(os.path.realpath(subclass.filename))
        day = int(subclass_file.parent.stem)
        year = int(subclass_file.parent.parent.stem)

        return year, day

    @abstractmethod
    def parse(self, raw: str):
        raise NotImplementedError

    @abstractmethod
    def part1(self, data):
        raise NotImplementedError

    @abstractmethod
    def part2(self, data):
        raise NotImplementedError

    def solve(self, part: int, testing: bool = True):
        raw = self._get_data(testing)
        data = self.parse(raw)

        match part:
            case 1:
                output = self.part1(data)
            case 2:
                output = self.part2(data)
            case _:
                raise ValueError(f"Invalid part number: {part}")

        print(output)


if __name__ == "__main__":
    raise TypeError("The class in this module must be subclassed and instantiated!")
