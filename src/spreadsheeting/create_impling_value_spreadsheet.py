import datetime
import time

from . import open_workbook, open_sheet, save_workbook
from . import SpreadsheetPage

from ..config.config import date_format

from ..data.implings import Impling
from ..data.impling_storage import load_values

def create_impling_value_spreadsheet():
    wb = open_workbook()
    impling_sheet = open_sheet(wb, SpreadsheetPage.IMPLINGS)

    impling_data = load_values()
    first_impling_data = impling_data[str(Impling.BABY.value)]
    columns_per_impling = len(first_impling_data.keys()) * 2

    for index, impling in enumerate(Impling):

        impling_sheet.cell(column=columns_per_impling * index + 1, row=1, value=impling.name)

        for column_index, value_type in enumerate(impling_data[str(impling.value)].keys()):
            impling_sheet.cell(column=columns_per_impling * index + 1 + column_index * 2, row=2, value=value_type)
            impling_sheet.cell(column=columns_per_impling * index + 1 + column_index * 2, row=3, value="date")
            impling_sheet.cell(column=columns_per_impling * index + 1 + column_index * 2 + 1, row=3, value="value")

            for row_index, timestamp in enumerate(impling_data[str(impling.value)][value_type].keys()):

                date = datetime.datetime.fromtimestamp(int(timestamp)/1000)
                formatted_date = f'"{date.strftime(date_format)}"'

                impling_value = impling_data[str(impling.value)][value_type][timestamp]

                impling_sheet.cell(column=columns_per_impling * index + 1 + column_index * 2, row=4 + row_index, value=formatted_date)
                impling_sheet.cell(column=columns_per_impling * index + 1 + column_index * 2 + 1, row=4 + row_index, value=impling_value)

    save_workbook(wb)