from datetime import datetime

from ..data.implings import Impling
from ..data.scrolls import Scroll

from ..data.casket_storage import load_time_values as load_casket_data
from ..jobs.store_casket_api_data import store_casket_api_data

from ..data.jar_storage import load_time_values as load_jar_data
from ..jobs.store_jar_value import store_jar_api_data

from ..data.scroll_chance_storage import load_time_values as load_scroll_data
from ..jobs.store_scroll_chance import store_scroll_chance_api_data


def handle_data():
    now = datetime.now()

    casket_data = load_casket_data()
    max_time = max(list(map(int, casket_data[Scroll.EASY.name].keys())))
    if (datetime.fromtimestamp(max_time) - now).seconds * 60 * 60 < 1:
        store_casket_api_data(int(now.timestamp()))

    jar_data = load_jar_data()
    max_time = max(list(map(int, jar_data[Impling.BABY.name].keys())))
    if (datetime.fromtimestamp(max_time) - now).seconds * 60 * 60 < 1:
        store_jar_api_data(int(now.timestamp()))

    scroll_data = load_scroll_data()
    max_time = max(list(map(int, scroll_data[Impling.BABY.name].keys())))
    if (datetime.fromtimestamp(max_time) - now).seconds * 60 * 60 < 1:
        store_scroll_chance_api_data(int(now.timestamp()))