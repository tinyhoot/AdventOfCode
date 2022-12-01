# A base class for solutions during Advent of Code.
import inspect
import logging
import os
import sys
from abc import ABCMeta, abstractmethod
from pathlib import Path

from utils import constants, filehandler


class Solution(metaclass=ABCMeta):

    def __init__(self):
        self._log = logging.getLogger(constants.ROOT_LOGGER)
        self._log.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("{levelname}:{name}:{message}", style="{"))
        self._log.addHandler(handler)

    def _get_data(self, test_data: bool = True) -> str:
        year, day = self._get_day()
        if test_data:
            return filehandler.get_test_input(year, day)
        else:
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

    def solve(self, testing: bool = True):
        raw = self._get_data(testing)
        data = self.parse(raw)

        self._log.info("---------- PART 1 OUTPUT ----------")
        print(self.part1(data))
        self._log.info("---------- PART 2 OUTPUT ----------")
        print(self.part2(data))


if __name__ == "__main__":
    raise TypeError("The class in this module must be subclassed and instantiated!")
