from ..data.impling_storage import load_values, save_values
from ..data.implings import Impling
from ..jobs.retrieve_impling_value import retrieve_impling_value

def store_impling_api_data():
    data = load_values()
    for impling in Impling:
        if impling.value not in data.keys():
            data[impling.value] = {}

        impling_data = retrieve_impling_value(impling)
        for key, value in impling_data.items():
            data[impling.value][key] = {}
            for timestamp, value in impling_data[key].items():
                data[impling.value][key][timestamp] = value
    save_values(data)