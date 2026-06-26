import json
from pathlib import Path

import yaml


def read_file(path):
    extension = Path(path).suffix
    if extension == '.json':
        with open(path) as open_file:
            return json.load(open_file)
    
    elif extension == '.yml' or extension == '.yaml':
        with open(path) as open_file:
            return yaml.safe_load(open_file)