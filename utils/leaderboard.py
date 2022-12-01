import json
import logging

from utils import constants, filehandler, misc
from utils.api import APIHandler


class Leaderboard:

    def __init__(self, year: int):
        self.year = year
        self._log = logging.getLogger(constants.ROOT_LOGGER + "." + __name__)

    def _get_leaderboard(self) -> dict:
        """Get the leaderboard JSON data from cache or online."""
        url = constants.LEADERBOARD_URL.format(self.year, constants.USER_ID)
        cache, timestamp = filehandler.load_cache(url)

        # If the cache is missing or old, redownload.
        if cache and misc.unix_now() - timestamp <= constants.REFRESH_RATE:
            data = cache
        else:
            self._log.info("Cache was old or missing, redownloading.")
            api_handler = APIHandler(filehandler.get_session_cookie())
            data = api_handler.get_leaderboard(self.year)
            filehandler.save_cache(data, url)

        return json.loads(data)

    def update(self):
        data = self._get_leaderboard()

        print(data)
        print("yehh")


if __name__ == "__main__":
    lb = Leaderboard(2022)
    lb.update()
