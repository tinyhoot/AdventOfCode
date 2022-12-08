import importlib
import logging
import sys
from argparse import ArgumentParser

from utils import constants, filehandler

_log = logging.getLogger(constants.ROOT_LOGGER)


def _cli_next(args):
    next_day = filehandler.get_latest_day(args.year) + 1
    filehandler.setup_day(args.year, next_day)


def _cli_run(args):
    run(2022, args.day, args.test_input)


def get_cli() -> ArgumentParser:
    """Get the command line interface for this project."""
    parser = ArgumentParser(description="Advent of Code")
    subparsers = parser.add_subparsers()

    next_parser = subparsers.add_parser("next", help="create files for a new day")
    next_parser.set_defaults(func=_cli_next)
    next_parser.add_argument("year", nargs="?", type=int, default=2022, help="the year to create a new day for")

    run_parser = subparsers.add_parser("run", help="run the solution for a specific day")
    run_parser.set_defaults(func=_cli_run)
    # run_parser.add_argument("year", type=int, default=2022, help="the year of AoC to select")
    run_parser.add_argument("day", nargs="?", type=int, default=-1, help="the day of AoC to run")
    run_parser.add_argument("-t", "--test-input", action="store_true", help="if passed, run on test input only")

    return parser


def main():
    parser = get_cli()
    args = parser.parse_args()
    setup_logger()
    # Execute the function corresponding to the chosen subcommand.
    args.func(args)


def run(year: int, day: int, test_input: bool):
    """Run the solution for a specific day."""
    if day < 0:
        day = filehandler.get_latest_day(year)
    _log.info(f"Running AoC {year} Day {day}")
    module = importlib.import_module(f"{year}.{day:02}.solution")
    solution = module.Solution()
    solution.solve(test_input)


def setup_logger():
    _log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("{levelname}:{name}:{message}", style="{"))
    _log.addHandler(handler)


if __name__ == "__main__":
    main()
