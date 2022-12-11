# A base class for solutions during Advent of Code.
import copy
import logging
import os
from abc import ABCMeta, abstractmethod
from pathlib import Path

from utils import constants, filehandler


class BaseSolution(metaclass=ABCMeta):

    def __init__(self):
        self._log = logging.getLogger(constants.ROOT_LOGGER + "." + __name__)

    def _get_data(self, test_data: bool = True) -> str:
        year, day = self._get_day()
        if test_data:
            return filehandler.get_test_input(year, day)
        else:
            return filehandler.get_puzzle_input(year, day)

    def _get_day(self) -> (int, int):
        """Get the correct year and day based on the filepath of the executing subclass."""
        subclass = self.__module__
        subclass_file = Path(os.path.realpath(subclass.replace(".", "/")))
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
        part1data = copy.deepcopy(data)

        self._log.info("---------- PART 1 OUTPUT ----------")
        print(self.part1(part1data))
        self._log.info("---------- PART 2 OUTPUT ----------")
        print(self.part2(data))


if __name__ == "__main__":
    raise TypeError("The class in this module must be subclassed and instantiated!")
