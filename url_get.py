import os

import requests

from Dmhylib import log


def get_url(url,
            proxies=None,
            system_proxy=False,
            verify=True):
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }

    if system_proxy:
        proxies = {
            'http': os.environ.get('http_proxy'),
            'https': os.environ.get('https_proxy')
        }

        if not proxies['http'] or not proxies['https']:
            log.warning("No system proxy found")
            proxies = None

    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url,
                                headers=headers,
                                proxies=proxies,
                                verify=verify)
        log.debug(f"A request has been made to url: {url}")

    except Exception as e:
        log.exception("The search was aborted due to some network reasons:")
        raise e

    return response.content
