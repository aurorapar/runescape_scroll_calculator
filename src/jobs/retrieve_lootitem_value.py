import requests

from ..data.loot_items import LootItem


def retrieve_lootitem_value(lootitem):
    if lootitem not in [i for i in LootItem]:
        raise RuntimeError(f'Lootitem {lootitem} is not supported')
    url = "https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={0}".format(lootitem.value)

    header = {"User-Agent": "scroll_calculator"}
    response = requests.get(url)

    if response.status_code not in [200]:
        raise RuntimeError(f'Could not retrieve data for lootitem {lootitem}, responses:\r\n{response.url}\r\n{response.text}\r\n{response.status_code}\r\n{response.reason}')

    return response.json()