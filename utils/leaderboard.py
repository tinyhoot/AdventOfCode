import json
import logging
import re

from utils import constants, filehandler, misc
from utils.api import APIHandler


README_STAR = "\u2728"


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

    def _readme_row(self, day: int, timestamp: int = None, stars: int = None) -> str:
        """Generate one row of the table in the readme's progress section."""
        day_str = str(day) if day >= 10 else "0" + str(day)
        day_link = constants.DAY_URL.format(self.year, day)
        day_cell = f"[{day_str}]({day_link})"

        if timestamp is not None:
            time_cell = misc.ts_to_hours(timestamp, misc.unix_unlock_time(self.year, day))
        else:
            time_cell = "N/A"

        if stars is not None:
            star_cell = README_STAR * stars
        else:
            star_cell = "-"

        return f"| {day_cell} | {time_cell} | {star_cell} |\n"

    def _readme_table(self, data: dict) -> str:
        """Assemble the entire progress table for the readme file."""
        user = data["members"][str(constants.USER_ID)]
        days = user["completion_day_level"]
        rows = []

        # Try to parse the JSON dictionary for each day.
        for day in range(1, 26):
            day_info = days.get(str(day))
            if not day_info:
                rows.append(self._readme_row(day))
                continue
            part_one = day_info.get("1")
            part_two = day_info.get("2")
            stars = 1
            timestamp = part_one.get("get_star_ts")
            if part_two:
                stars += 1
                timestamp = part_two.get("get_star_ts")
            rows.append(self._readme_row(day, timestamp, stars))

        return "".join(rows)

    def update(self):
        data = self._get_leaderboard()
        self._update_readme(data)

    def _update_readme(self, data: dict):
        """Update the project's README file with the given JSON data."""
        with open(filehandler.get_base_dir() / "README.md", "r+", encoding="utf-8") as readme:
            contents = readme.read()
            # Find and modify the table containing daily results.
            lookup = re.search("# Progress.*---:?\\|\n(.*)\n<!--- EndProgress -->", contents, flags=re.DOTALL)
            table = self._readme_table(data)
            new_contents = contents[:lookup.span(1)[0]] + table + contents[lookup.span(1)[1]:]
            # Delete the old contents, replace it with the new.
            readme.seek(0)
            readme.truncate()
            readme.write(new_contents)
            self._log.info("Updated README file.")


if __name__ == "__main__":
    lb = Leaderboard(2022)
    lb.update()
