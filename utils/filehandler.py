# Anything to do with file handling inside the project directory goes here.
import datetime as dt
import logging
import os
from datetime import datetime
from pathlib import Path

from utils import api, constants
from utils.errors import ImpatientError

PUZZLE_INPUT_FILENAME = "puzzle_input.txt"
SESSION_COOKIE_FILENAME = "session_cookie"
_log = logging.getLogger(constants.ROOT_LOGGER + "." + __name__)


def check_date(year: int, day: int) -> dt.timedelta:
    target = datetime(year, 12, day, 5)
    return target - datetime.utcnow()


def get_base_dir() -> Path:
    """Get the project base directory."""
    # Hardcoded and relies on a specific file structure, but that's fine.
    this_file = Path(os.path.realpath(__file__))
    return this_file.parent.parent


def get_day_dir(year: int, day: int) -> Path:
    """Get the directory for a specific day."""
    year_str = str(year)
    day_str = str(day) if day >= 10 else "0" + str(day)
    return get_base_dir() / year_str / day_str


def get_puzzle_input(year: int, day: int) -> str:
    """Get the puzzle input for a specific day. Download it if it does not already exist."""
    unlock_time = check_date(year, day)
    if unlock_time.total_seconds() > 0:
        raise ImpatientError(f"Be patient! The puzzle for {year}-12-{day} unlocks in {unlock_time}")

    puzzle_file = get_day_dir(year, day) / PUZZLE_INPUT_FILENAME
    _log.info(f"Grabbing puzzle input from file: {puzzle_file}")

    if not puzzle_file.exists():
        _log.warning(f"No puzzle file found for {year}-{day}, downloading.")
        cookie = get_session_cookie()
        data = api.get_puzzle_input(year, day, cookie)
        save_puzzle_input(data, year, day)

    with open(puzzle_file, "r", encoding="utf-8") as file:
        data = file.read()

    return data


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


def save_puzzle_input(data, year: int, day: int):
    dir_path = get_day_dir(year, day)
    file_path = dir_path / PUZZLE_INPUT_FILENAME

    dir_path.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data)
    _log.info(f"Saved puzzle input to disk for {year}-{day}")
