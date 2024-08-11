import csv
import os
import re
import time
from collections import OrderedDict
from typing import List, Optional, Tuple
from urllib.parse import urlencode, urlparse, parse_qs

from bs4 import BeautifulSoup

from . import log
from .url_get import get_url

size_pattern = re.compile(r'(\d+(?:\.\d+)?)\s*(\w+)')

conversion_factors = OrderedDict([
    ('B', 1),
    ('KB', 1024),
    ('MB', 1048576),
    ('GB', 1073741824),
    ('TB', 1099511627776)
])

AVAILABLE_SORT_IDS = [0, 2, 31, 3, 41, 42, 4, 43, 44, 15, 6, 7, 9, 17, 18, 19, 20, 21, 12, 1]
BASE_URL = "https://dmhy.org/topics/list/page/{}?"


class DmhySearch:
    def __init__(self, parser: str = 'lxml', verify: bool = True, timefmt: str = '%Y/%m/%d %H:%M'):
        self.reset()

        self._parser = parser
        self._verify = verify
        self.set_timefmt(timefmt)
        log.debug("New search object created.")

    def set_timefmt(self, timefmt: str) -> None:
        """Set and validate the time format."""
        try:
            # Validate the time format by attempting to use it
            time.strftime(timefmt, time.localtime())
            self._timefmt = timefmt
            self.is_default_format = timefmt == '%Y/%m/%d %H:%M'
        except ValueError:
            raise ValueError(f"Invalid time format: {timefmt}")

    def reset(self) -> None:
        self.sum = 0
        self.times: List[str] = []
        self.titles: List[str] = []
        self.sizes: List[str] = []
        self.magnets: List[str] = []
        self.time = ""
        self.title = ""
        self.size = ""
        self.magnet = ""
        self.if_selected = False

    def search(self, keyword: str, sort_id: int = 0, team_id: int = 0, order: str = 'date-desc',
               proxies: Optional[dict] = None, system_proxy: bool = False) -> None:
        if sort_id not in AVAILABLE_SORT_IDS:
            raise ValueError(f"'{sort_id}' is not a valid sort_id")

        self.reset()
        params = urlencode({
            'keyword': keyword,
            'sort_id': sort_id,
            'team_id': team_id,
            'order': order
        })

        for page in range(1, 1000):
            url = BASE_URL.format(page) + params
            html = get_url(url, verify=self._verify, proxies=proxies, system_proxy=system_proxy)
            bs = BeautifulSoup(html, self._parser)
            working = bs.find(id="topic_list")

            if not working:
                break

            for tr in working.tbody.find_all("tr"):
                tds = tr.find_all("td")
                self.sum += 1

                release_time = tds[0].span.content
                if not self.is_default_format:
                    release_time = time.strftime(self._timefmt, time.strptime(release_time, '%Y/%m/%d %H:%M'))
                self.times.append(release_time)

                title = tds[2].find_all("a")[-1].get_text().strip()
                self.titles.append(title)

                url = tds[3].find(class_="download-pp").get("href")
                magnet = parse_qs(urlparse(url).query)['url'][0]
                self.magnets.append(magnet)

                self.sizes.append(tds[4].string)

                log.debug(f"Successfully got: {title}")

        log.info(f"This search is complete: {keyword}")

    def select(self, num: int) -> None:
        if num < 0 or num >= len(self.times):
            raise IndexError("Invalid selection index")
        self.time = self.times[num]
        self.title = self.titles[num]
        self.size = self.sizes[num]
        self.magnet = self.magnets[num]
        self.if_selected = True

    def size_format(self, unit='MB') -> None:
        if not self.if_selected:
            raise ValueError("No item selected. Please use select() method first.")

        self.value, self.unit = self.extract_value_and_unit(self.size)
        if self.unit != unit:
            self.value = self.convert_byte(self.value, self.unit, unit)
            self.size = f"{self.value}{unit}"

    def save_csv(self, filename: str) -> None:
        if not self.if_selected:
            raise ValueError("No item selected. Please use select() method first.")

        fieldnames = ["time", "title", "size", "magnet"]
        file_exists = os.path.exists(filename)

        with open(filename, mode='a+', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "time": self.time,
                "title": self.title,
                "size": self.size,
                "magnet": self.magnet
            })

    @staticmethod
    def convert_byte(value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert a byte value from one unit to another.

        Args:
            value (float): The value to convert.
            from_unit (str): The unit to convert from.
            to_unit (str): The unit to convert to.

        Returns:
            float: The converted value.

        Raises:
            ValueError: If an invalid storage unit is provided.
        """
        try:
            from_factor = conversion_factors[from_unit.upper()]
            to_factor = conversion_factors[to_unit.upper()]
        except KeyError as e:
            log.critical("This error may mean that the program has not worked as expected:")
            raise ValueError(f"Convert: invalid storage unit '{e.args[0]}'") from e

        return round(value * (from_factor / to_factor), 2)

    @staticmethod
    def extract_value_and_unit(size: str) -> Tuple[float, str]:
        """
        Extract the numeric value and unit from a size string.

        Args:
            size (str): The size string to parse.

        Returns:
            Tuple[float, str]: The extracted value and unit.

        Raises:
            ValueError: If the size string is invalid.
        """
        match = size_pattern.match(size)

        if match:
            value = float(match.group(1))
            unit = match.group(2)
            return value, unit
        else:
            log.critical("This error may mean that the program has not worked as expected:")
            raise ValueError(f"Extract: invalid size '{size}'")


if __name__ == "__main__":
    import doctest
    doctest.testmod()