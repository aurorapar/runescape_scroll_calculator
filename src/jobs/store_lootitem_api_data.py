from ..data.lootitem_storage import load_values, save_values
from ..data.loot_items import LootItem
from ..jobs.retrieve_lootitem_value import retrieve_lootitem_value

def store_lootitem_api_data():
    data = load_values()
    for lootitem in LootItem:
        if lootitem.value not in data.keys():
            data[lootitem.value] = {}
        print(f"Retrieving data for {lootitem.name} lootitem")
        lootitem_data = retrieve_lootitem_value(lootitem)
        for key, value in lootitem_data.items():
            data[lootitem.value][key] = {}
            for timestamp, value in lootitem_data[key].items():
                data[lootitem.value][key][timestamp] = value
    save_values(data)