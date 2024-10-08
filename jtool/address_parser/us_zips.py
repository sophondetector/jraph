from typing import Union
import json

_ZIP2CITY_MAP = None
_ZIP2STATE_MAP = None


def _load_zip2city() -> dict:
    global _ZIP2CITY_MAP
    if _ZIP2CITY_MAP is None:
        with open('lib/data/zip2city.json') as fh:
            _ZIP2CITY_MAP = json.load(fh)
    return _ZIP2CITY_MAP


def _load_zip2state() -> dict:
    global _ZIP2STATE_MAP
    if _ZIP2STATE_MAP is None:
        with open('lib/data/zip2state.json') as fh:
            _ZIP2STATE_MAP = json.load(fh)
    return _ZIP2STATE_MAP


def zip2city(zip: Union[str, int]) -> str:
    if type(zip) is int:
        zip = str(zip)
    zip = zip[:5]
    return _load_zip2city().get(zip)


def zip2state(zip: Union[str, int]) -> str:
    if type(zip) is int:
        zip = str(zip)
    zip = zip[:5]
    return _load_zip2state().get(zip)
