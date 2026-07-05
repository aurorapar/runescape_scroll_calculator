from . import open_workbook, open_sheet, save_workbook
from . import SpreadsheetPage

from ..config.config import price_suffixes

from ..data.loot_items import LootItem, LOOT_ITEM_QUALITIES
from ..data.lootitem_storage import load_values

from ..helpers.helpers import format_price

def create_lootitem_value_spreadsheet():
    wb = open_workbook()
    lootitem_sheet = open_sheet(wb, SpreadsheetPage.LOOT_ITEMS)

    lootitem_data = load_values()
    columns_per_lootitem = 4 #  max([len(table.keys()) for table in LOOT_ITEM_QUALITIES.values()])

    lootitem_sheet.cell(column=2, row=1, value="quantity(ies)")
    lootitem_sheet.cell(column=3, row=1, value="rarity")
    lootitem_sheet.cell(column=4, row=1, value="price")
    lootitem_sheet.cell(column=5, row=1, value="adjusted price")

    for index, lootitem in enumerate(LootItem):

        lootitem_sheet.cell(column=1, row=index+2, value=lootitem_data[str(lootitem.value)]["item"]["name"])

        quantity = LOOT_ITEM_QUALITIES[lootitem]["quantities"] if "quantities" in LOOT_ITEM_QUALITIES[lootitem].keys() else LOOT_ITEM_QUALITIES[lootitem]["quantity"]
        lootitem_sheet.cell(column=2, row=index+2, value=f"{quantity[0]}-{quantity[1]}" if not isinstance(quantity,int) else quantity)

        lootitem_sheet.cell(column=3, row=index+2, value=LOOT_ITEM_QUALITIES[lootitem]["rarity"])

        price = lootitem_data[str(lootitem.value)]["item"]["current"]["price"]
        lootitem_sheet.cell(column=4, row=index+2, value=lootitem_data[str(lootitem.value)]["item"]["current"]["price"])

        adjusted_price = 0

        price = format_price(price)

        if isinstance(quantity,int):
            adjusted_price = quantity * LOOT_ITEM_QUALITIES[lootitem]["rarity"] * price
        else:
            adjusted_price = (quantity[0] + quantity[1]) / 2 * LOOT_ITEM_QUALITIES[lootitem]["rarity"] * price
        lootitem_sheet.cell(column=5, row=index+2, value=adjusted_price)

    save_workbook(wb)