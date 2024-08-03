import logging

logging.basicConfig(format="")
log = logging.getLogger("global")
log.setLevel(logging.DEBUG)

fh = logging.FileHandler("dmhy.log", mode='w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
log.addHandler(fh)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
log.addHandler(sh)

from Dmhylib.DmhySearch import DmhySearch, SORT_ID_COLLECTION
__all__ = ["DmhySearch", "SORT_ID_COLLECTION", "log"]