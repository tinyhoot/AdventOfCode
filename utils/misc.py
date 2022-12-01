# Common things that are useful, but don't fit anywhere else.
from datetime import datetime

from utils import constants


def is_unlocked(year: int, day: int) -> bool:
    """Check whether the puzzle for a specific date has already unlocked."""
    return unix_unlock_time(year, day) - unix_now() < 0


def ts_to_hours(timestamp: int, other_time: int) -> str:
    """Take two timestamps and convert their time difference to a string hh:mm:ss"""
    d1 = datetime.fromtimestamp(timestamp)
    d2 = datetime.fromtimestamp(other_time)
    diff = abs(int((d1 - d2).total_seconds()))

    mins, secs = divmod(diff, 60)
    hrs, mins = divmod(mins, 60)
    return f"{hrs:02}:{mins:02}:{secs:02}"


def unix_now() -> int:
    """Get the UNIX timestamp for right now."""
    return int(datetime.now().timestamp())


def unix_unlock_time(year: int, day: int) -> int:
    """Get the UNIX timestamp for the unlock time of a specific day."""
    return int(datetime(year, 12, day, constants.UNLOCK_OFFSET).timestamp())
