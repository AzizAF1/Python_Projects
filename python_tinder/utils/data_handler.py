import json
import os

def load_data(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
