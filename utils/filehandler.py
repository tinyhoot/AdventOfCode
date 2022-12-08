# Anything to do with file handling inside the project directory goes here.
import logging
import os
import shutil
from pathlib import Path
import re

from utils import constants, misc
from utils.api import APIHandler
from utils.errors import ImpatientError

PUZZLE_INPUT_FILENAME = "puzzle_input.txt"
SOLUTION_FILENAME = "solution.py"
TEST_INPUT_FILENAME = "test_input.txt"
SESSION_COOKIE_FILENAME = "session_cookie"
_log = logging.getLogger(constants.ROOT_LOGGER + "." + __name__)


def get_base_dir() -> Path:
    """Get the project base directory."""
    # Hardcoded and relies on a specific file structure, but that's fine.
    this_file = Path(os.path.realpath(__file__))
    return this_file.parent.parent


def get_cache_dir() -> Path:
    return get_base_dir() / constants.CACHE_DIR


def get_day_dir(year: int, day: int) -> Path:
    """Get the directory for a specific day."""
    year_str = str(year)
    day_str = str(day) if day >= 10 else "0" + str(day)
    return get_base_dir() / year_str / day_str


def get_latest_day(year: int) -> int:
    """Get the latest day that exists for the given year."""
    year_dir = get_base_dir() / str(year)
    latest = -1
    for child in year_dir.iterdir():
        if child.is_dir():
            try:
                day = int(child.name)
                latest = day if day > latest else latest
            except ValueError:
                continue

    if latest == -1:
        raise FileNotFoundError(f"No day directories exist for year {year}!")
    return latest


def get_puzzle_input(year: int, day: int) -> str:
    """Get the puzzle input for a specific day. Download it if it does not already exist."""
    if not misc.is_unlocked(year, day):
        raise ImpatientError(f"Be patient! The puzzle for {year}-12-{day} unlocks at 5am UTC.")

    puzzle_file = get_day_dir(year, day) / PUZZLE_INPUT_FILENAME
    _log.info(f"Grabbing puzzle input from file: {puzzle_file}")

    if puzzle_file.exists():
        with open(puzzle_file, "r", encoding="utf-8") as file:
            data = file.read()
    else:
        _log.warning(f"No puzzle file found for {year}-{day}, downloading.")
        api_handler = APIHandler(get_session_cookie())
        data = api_handler.get_puzzle_input(year, day)
        save_puzzle_input(data, year, day)

    return data


def get_solution(year: int, day: int) -> Path:
    """Get the solution file for a specific day."""
    return get_day_dir(year, day) / SOLUTION_FILENAME


def get_solution_template() -> Path:
    return get_base_dir() / ".idea" / "fileTemplates" / "Advent of Code Template.py"


def get_test_input(year: int, day: int) -> str:
    """Get the testing input for a specific day."""
    test_file = get_day_dir(year, day) / TEST_INPUT_FILENAME
    _log.info(f"Grabbing test input from file: {test_file}")
    if test_file.exists():
        with open(test_file, "r", encoding="utf-8") as file:
            data = file.read()
        return data
    else:
        raise FileNotFoundError(f"Failed to find test input file at {test_file}")


def get_session_cookie() -> str:
    path = _get_session_cookie_file()
    with open(path, "r", encoding="utf-8") as file:
        cookie = file.read()

    return cookie


def _get_session_cookie_file() -> Path:
    cookie_file = get_base_dir() / SESSION_COOKIE_FILENAME
    if not cookie_file.exists():
        raise FileNotFoundError(f"No session cookie file exists. Create a '{SESSION_COOKIE_FILENAME}' file in this"
                                f"project's root directory and store a valid cookie there to proceed.")

    return cookie_file


def load_cache(url: str) -> tuple[str, int] | tuple[None, None]:
    path = _url_to_filename(url)
    cached_files = sorted(path.parent.glob(f"{path.name}-*"), reverse=True, key=lambda x: int(x.name.split("-")[1]))
    if not cached_files:
        _log.info(f"Found no cache for {path}")
        return None, None

    # Load only the latest file.
    with open(cached_files[0], "r", encoding="utf-8") as file:
        data = file.read()
    timestamp = int(cached_files[0].name.split("-")[1])
    return data, timestamp


def save_cache(data, url: str):
    path = _url_to_filename(url)
    # Add a timestamp.
    timestamp = int(misc.unix_now())
    path = path.with_name(f"{path.name}-{timestamp}")

    get_cache_dir().mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(data)
        _log.info(f"Wrote cache to disk at {path.name}")


def save_puzzle_input(data, year: int, day: int):
    dir_path = get_day_dir(year, day)
    file_path = dir_path / PUZZLE_INPUT_FILENAME

    dir_path.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data)
    _log.info(f"Saved puzzle input to disk for {year}-{day}")


def setup_day(year: int, day: int):
    """Set up all the template files for the specific day and year."""
    day_dir = get_day_dir(year, day)
    if day_dir.exists():
        raise ValueError(f"The directory for {year} Day {day} already exists!")
    day_dir.mkdir(parents=True)
    test_input = day_dir / TEST_INPUT_FILENAME
    test_input.touch()
    shutil.copy2(get_solution_template(), get_solution(year, day))


def _url_to_filename(url: str) -> Path:
    # Drop the domain and filename, replace slashes.
    filename = re.search(".com/(.*).json", url)[1]
    filename = re.sub("/", "_", filename)
    return get_cache_dir() / filename
