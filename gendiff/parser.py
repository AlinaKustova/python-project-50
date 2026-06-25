import json
from pathlib import Path


def read_file(path):
    extension = Path(path).suffix
    if extension == '.json':
        with open(path) as open_file:
            return json.load(open_file)