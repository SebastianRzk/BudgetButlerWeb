import json

from butler_offline.core import file_system
from butler_offline.core.shares import SharesInfo

SHARES_PATH = './shares_info_cache.json'


def save_if_needed(shares_data):
    if not shares_data.is_changed():
        return
    file_system.instance().write(SHARES_PATH, json.dumps(shares_data.content))


def load_data():
    data = file_system.instance().read(SHARES_PATH)
    if not data:
        return SharesInfo({})
    return SharesInfo(json.loads(''.join(data)))
