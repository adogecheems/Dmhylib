import csv
import os
from typing import List, Optional
from urllib.parse import urlencode, urlparse, parse_qs

from bs4 import BeautifulSoup

from dmhylib import log
from dmhylib.byte_convert import extract_value_and_unit, convert_byte
from dmhylib.url_get import get_url

AVAILABLE_SORT_IDS = [0, 2, 31, 3, 41, 42, 4, 43, 44, 15, 6, 7, 9, 17, 18, 19, 20, 21, 12, 1]
SORT_ID_COLLECTION = 31
BASE_URL = "https://dmhy.org/topics/list/page/{}?"


class DmhySearch:
    def __init__(self, parser: str = 'lxml', verify: bool = True):
        self.reset()
        self._parser = parser
        self._verify = verify
        log.debug("New search object created.")

    def reset(self) -> None:
        self.sum = 0

        self.titles: List[str] = []
        self.pikpak_urls: List[str] = []
        self.sizes: List[str] = []
        self.magnets: List[str] = []

        self.title = ""
        self.pikpak_url = ""
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

        for page in range(1, 1000):  # Assuming a reasonable maximum of 1000 pages
            url = BASE_URL.format(page) + params
            html = get_url(url, verify=self._verify, proxies=proxies, system_proxy=system_proxy)
            bs = BeautifulSoup(html, self._parser)
            working = bs.find(id="topic_list")

            if working:
                for tr in bs.find(id="topic_list").tbody.find_all("tr"):
                    tds = tr.find_all("td")

                    self.sum += 1

                    try:
                        title = tds[2].find_all("a")[1].get_text()
                    except IndexError:
                        title = tds[2].find_all("a")[0].get_text()

                    title = "".join(char for char in title if not char.isspace())
                    self.titles.append(title)

                    url = tds[3].find(class_="download-pp").get("href")
                    self.pikpak_urls.append(url)

                    magnet = parse_qs(urlparse(url).query)['url'][0]
                    self.magnets.append(magnet)

                    self.sizes.append(tds[4].string)

                    log.debug(f"Successfully got: {title}")
            else:
                break

        log.info(f"This search is complete: {keyword}")

    def select(self, num: int) -> None:
        self.title = self.titles[num]
        self.pikpak_url = self.pikpak_urls[num]
        self.size = self.sizes[num]
        self.magnet = self.magnets[num]
        self.if_selected = True

    def size_format(self) -> None:
        if not self.if_selected:
            raise ValueError("No item selected. Please use select() method first.")

        self.value, self.unit = extract_value_and_unit(self.size)
        if self.unit != 'MB':
            self.value = convert_byte(self.value, self.unit, 'MB')
            self.size = f"{self.value}MB"

    def save_csv(self, filename: str) -> None:
        if not self.if_selected:
            raise ValueError("No item selected. Please use select() method first.")

        if not os.path.exists(filename):
            with open(filename, mode='w') as f:
                f.write("title,pikpak_url,size,magnet\n")

        with open(filename, mode='a+') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "title",
                "pikpak_url",
                "size",
                "magnet"
            ])

            writer.writerow({
                "title": self.title,
                "pikpak_url": self.pikpak_url,
                "size": self.size,
                "magnet": self.magnet
            })


if __name__ == "__main__":
    import doctest

    doctest.testmod()
