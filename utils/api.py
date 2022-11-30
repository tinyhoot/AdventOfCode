# Anything that needs or tries to interact with the AdventOfCode webpage goes here.
import logging

import requests

from utils import constants

INPUT_URL = "https://adventofcode.com/{}/day/{}/input"
_log = logging.getLogger(constants.ROOT_LOGGER + "." + __name__)


def get_puzzle_input(year: int, day: int, cookie: str) -> str:
    url = INPUT_URL.format(year, day)

    _log.info(f"Requesting puzzle input from {url}")
    response = requests.get(url, cookies={"session": cookie})
    if response.status_code == 200:
        return response.text

    _log.fatal(f"Unexpected response from server: {response.status_code} {response.reason}")
    raise ConnectionError(f"Bad response from AoC: {response.status_code} {response.reason}")
