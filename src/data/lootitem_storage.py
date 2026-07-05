import json
import os

STORAGE_FILE = "lootitem_values.json"

def load_values():
    if STORAGE_FILE not in os.listdir():
        create_storage_file()

    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def save_values(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f)

def create_storage_file():
    with open(STORAGE_FILE, "w") as f:
        json.dump({}, f)