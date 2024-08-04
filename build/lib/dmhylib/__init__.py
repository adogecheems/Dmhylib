import logging
from typing import List

# 常量定义
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
LOG_FILE = "dmhy.log"


def setup_logger(name: str = "global", level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(LOG_FILE, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


log = setup_logger()

from dmhylib.DmhySearch import DmhySearch, SORT_ID_COLLECTION

__all__: List[str] = ["DmhySearch", "SORT_ID_COLLECTION", "log"]
