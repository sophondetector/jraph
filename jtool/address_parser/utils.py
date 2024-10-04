from typing import Union
import json

_US_STATE_TUPLES = [
    ("alabama", "al"),
    ("kentucky", "ky"),
    ("ohio", "oh"),
    ("alaska", "ak"),
    ("louisiana", "la"),
    ("oklahoma", "ok"),
    ("arizona", "az"),
    ("maine", "me"),
    ("oregon", "or"),
    ("arkansas", "ar"),
    ("maryland", "md"),
    ("pennsylvania", "pa"),
    ("american samoa", "as"),
    ("massachusetts", "ma"),
    ("puerto rico", "pr"),
    ("california", "ca"),
    ("michigan", "mi"),
    ("rhode island", "ri"),
    ("colorado", "co"),
    ("minnesota", "mn"),
    ("south carolina", "sc"),
    ("connecticut", "ct"),
    ("mississippi", "ms"),
    ("south dakota", "sd"),
    ("delaware", "de"),
    ("missouri", "mo"),
    ("tennessee", "tn"),
    ("district of columbia", "dc"),
    ("montana", "mt"),
    ("texas", "tx"),
    ("florida", "fl"),
    ("nebraska", "ne"),
    ("trust territories", "tt"),
    ("georgia", "ga"),
    ("nevada", "nv"),
    ("utah", "ut"),
    ("guam", "gu"),
    ("new hampshire", "nh"),
    ("vermont", "vt"),
    ("hawaii", "hi"),
    ("new jersey", "nj"),
    ("virginia", "va"),
    ("idaho", "id"),
    ("new mexico", "nm"),
    ("virgin islands", "vi"),
    ("illinois", "il"),
    ("new york", "ny"),
    ("washington", "wa"),
    ("indiana", "in"),
    ("north carolina", "nc"),
    ("west virginia", "wv"),
    ("iowa", "ia"),
    ("north dakota", "nd"),
    ("wisconsin", "wi"),
    ("kansas", "ks"),
    ("northern mariana islands", "mp"),
    ("wyoming", "wy"),
]

STATES_FULL = list(map(lambda t: t[0], _US_STATE_TUPLES))
STATES_ABBR = list(map(lambda t: t[1], _US_STATE_TUPLES))


_FULL2ABBR_MAP = {full: abbr for full, abbr in _US_STATE_TUPLES}
_ABBR2FULL_MAP = {abbr: full for full, abbr in _US_STATE_TUPLES}


def full2abbr(full: str, upper_case: bool = True) -> str:
    res = _FULL2ABBR_MAP.get(full.lower())
    if upper_case:
        return res.upper()
    return res


def abbr2full(abbr: str, title_case: bool = True) -> str:
    res = _ABBR2FULL_MAP.get(abbr.lower())
    if title_case:
        return res.title()
    return res


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
