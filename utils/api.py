# Anything that needs or tries to interact with the AdventOfCode webpage goes here.
import logging

import requests

from utils import constants

_log = logging.getLogger(constants.ROOT_LOGGER + "." + __name__)


class APIHandler:

    def __init__(self, session_cookie: str):
        self.session_cookie = session_cookie

    def get_leaderboard(self, year: int) -> str:
        url = constants.LEADERBOARD_URL.format(year)
        _log.info(f"Requesting leaderboard stats from {url}")
        return self._request_response(url)

    def get_puzzle_input(self, year: int, day: int) -> str:
        url = constants.INPUT_URL.format(year, day)
        _log.info(f"Requesting puzzle input from {url}")
        return self._request_response(url)

    def _request_response(self, url: str) -> str:
        response = requests.get(url, cookies={"session": self.session_cookie})
        if response.status_code == 200:
            return response.text

        _log.fatal(f"Unexpected response from server: {response.status_code} {response.reason}")
        raise ConnectionError(f"Bad response from AoC: {response.status_code} {response.reason}")
