from ..data.jar_storage import load_values, save_values

from ..jobs.retrieve_jar_value import retrieve_jar_loot_values

def store_jar_api_data(now):
    data = retrieve_jar_loot_values()
    save_values(data, now)