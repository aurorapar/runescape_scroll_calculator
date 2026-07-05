from ..data.casket_storage import load_values, save_values

from ..jobs.retrieve_casket_value import retrieve_casket_value

def store_casket_api_data(now):
    casket_data = retrieve_casket_value()
    save_values(casket_data, now)