"""Cached loaders for the JSON data files shipped with the package."""
from functools import lru_cache
from pathlib import Path
import json

_DATA_DIR = Path(__file__).parent / 'data'


@lru_cache(maxsize=None)
def load(name):
    """Load ``data/<name>.json`` once. The result is shared: never mutate it
    (callers that need to modify must ``copy.deepcopy`` first)."""
    with open(_DATA_DIR / f'{name}.json', 'r', encoding='utf-8') as file:
        return json.load(file)
