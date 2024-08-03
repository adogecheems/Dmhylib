import logging
from urllib.parse import urlencode, urlparse, parse_qs

from bs4 import BeautifulSoup

from Dmhylib.byte_convert import *
from Dmhylib.url_get import get_url

available_sort_ids = [0, 2, 31, 3, 41, 42, 4, 43, 44, 15, 6, 7, 9, 17, 18, 19, 20, 21, 12, 1]
SORT_ID_COLLECTION = 31


class DmhySearch:
    def __init__(self, parser='lxml', verify=True):
        """
        >>> from Dmhylib import *
        >>> api = DmhySearch(verify=False)
        >>> api.search("我推的孩子", sort_id=31)
        >>> api.num
        23
        """
        self.num = 0

        self.titles = []
        self.pikpak_urls = []
        self.sizes = []
        self.magnets = []

        self.title = ""
        self.pikpak_url = ""
        self.size = ""
        self.magnet = ""

        self._parser = parser
        self._verify = verify

        self.if_selected = False

        logging.debug("New serach object created")

    def search(self,
               keyword,
               sort_id=0,
               team_id=0,
               order='date-desc',
               proxies=None,
               system_proxy=False):

        if sort_id not in available_sort_ids:
            raise KeyError(f"'{sort_id}'is not a valid sort_id")

        parse = urlencode(
            {
                'keyword': keyword,
                'sort_id': sort_id,
                'team_id': team_id,
                'order': order
            }
        )

        self.__init__(self._parser, self._verify)
        c = 0
        while True:
            c += 1

            url = f"https://dmhy.org/topics/list/page/{c}?" + parse
            html = get_url(url, verify=self._verify, proxies=proxies, system_proxy=system_proxy)
            bs = BeautifulSoup(html, self._parser)
            working = bs.find(id="topic_list")

            if working:
                for tr in bs.find(id="topic_list").tbody.find_all("tr"):
                    tds = tr.find_all("td")

                    self.num += 1

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
                log.info(f"This search is complete: {keyword}")
                break

    def select(self, num):
        self.title = self.titles[num]
        self.pikpak_url = self.pikpak_urls[num]
        self.size = self.sizes[num]
        self.magnet = self.magnets[num]

    def size_format(self):
        self.value, self.unit = extract_value_and_unit(self.size)

        if self.value != 'MB':
            self.value = convert_byte(self.value, self.unit, 'MB')
            self.unit = 'MB'
            self.size = self.value + self.unit


if __name__ == "__main__":
    import doctest

    doctest.testmod()
