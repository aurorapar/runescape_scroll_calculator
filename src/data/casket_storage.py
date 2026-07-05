import json
import os

STORAGE_FILE = "casket_values.json"
TIMED_STORAGE_DATA = "casket_timed_values.json"


def load_values():
    for storage_file in [STORAGE_FILE, TIMED_STORAGE_DATA]:
        if storage_file not in os.listdir():
            create_storage_file(storage_file)

    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def load_time_values():
    for storage_file in [STORAGE_FILE, TIMED_STORAGE_DATA]:
        if storage_file not in os.listdir():
            create_storage_file(storage_file)

    with open(TIMED_STORAGE_DATA, "r") as f:
        return json.load(f)

def save_values(data, now):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f)

    data2 = load_time_values()
    for k, v in data.items():
        if k not in data2.keys():
            data2[k] = {}
        data2[k][now] = v
    with open(TIMED_STORAGE_DATA, "w") as f:
        json.dump(data2, f)

def create_storage_file(storage_file):
    with open(storage_file, "w") as f:
        json.dump({}, f)