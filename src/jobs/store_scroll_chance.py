from ..data.scroll_chance_storage import load_values, save_values

from ..jobs.retrieve_scroll_chance import retrieve_scroll_chance

def store_scroll_chance_api_data(now):
    scroll_data = retrieve_scroll_chance()
    save_values(scroll_data, now)