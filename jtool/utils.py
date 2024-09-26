from typing import List, Optional

import re

import pandas as pd


class UsStateTools:
    tups = [
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

    _FULL2ABBR_MAP = {full: abbr for full, abbr in tups}
    _ABBR2FULL_MAP = {abbr: full for full, abbr in tups}

    _FULL_STATE_REGEX = re.compile(
        r'\s+(' + '|'.join(full for full, abb in tups) + r')\s+',
        re.IGNORECASE
    )

    _ABBR_STATE_REGEX = re.compile(
        r'\s+(' + '|'.join(abb for full, abb in tups) + r')\s+',
        re.IGNORECASE
    )

    @classmethod
    def abbrs(cls) -> List[str]:
        return [abb for full, abb in cls.tups]

    @classmethod
    def fulls(cls) -> List[str]:
        return [full for full, abb in cls.tups]

    @classmethod
    def full2abbr(cls, full): return cls._FULL2ABBR_MAP.get(full)

    @classmethod
    def abbr2full(cls, abbr): return cls._ABBR2FULL_MAP.get(abbr)

    @classmethod
    def parse_state(cls, addr) -> Optional[str]:
        """always returns abbreviation"""
        full_res = cls._parse_full(addr)
        if full_res is not None:
            return cls.full2abbr(full_res)
        abb_res = cls._parse_abbr(addr)
        if abb_res is None:
            print('couldnt find state in address {}'.format(addr))
        return abb_res

    @classmethod
    def _parse_full(cls, addr) -> Optional[str]:
        mat = re.search(cls._FULL_STATE_REGEX, addr)
        if mat:
            return mat[0].strip()
        return None

    @classmethod
    def _parse_abbr(cls, addr) -> Optional[str]:
        mat = re.search(cls._ABBR_STATE_REGEX, addr)
        if mat:
            return mat[0].strip()
        return None


class DataTools:
    OFFSHORE_LEAKS_COLUMNS = [
        "name",
        "lat",
        "long",
        "node_id",
        "address",
        "_id",
        "original_name",
        "former_name",
        "jurisdiction",
        "jurisdiction_description",
        "company_type",
        "internal_id",
        "incorporation_date",
        "inactivation_date",
        "struck_off_date",
        "dorm_date",
        "status",
        "service_provider",
        "ibcRUC",
        "country_codes",
        "countries",
        "sourceID",
        "valid_until",
        "note",
        "zip",
        "zip_five",
        "state"
    ]


_SPACE_REGEX = re.compile(r'\s\s+')
_USA_REGEX = re.compile(r'\s*(usa|u s a|united states of america)\s+(si)?')
_REMOVE_TO_CLEAN_REGEX = re.compile(r'[^a-z0-9 ]')
_REVERSE_ZIP_REGEX = re.compile(r'(\d\d\d\d\-?)? ?(\d\d\d\d\d)')


def safe_clean_string(s):
    """
    ensures input is a string before proceeding
    if its not a string just returns input
    """
    if type(s) is not str:
        return s
    s = re.sub(_SPACE_REGEX, ' ', s)
    return re.sub(_REMOVE_TO_CLEAN_REGEX, '', s.lower())


def clean_dataframe_strings(df, subset=None):
    """
    runs safe_clean_string on all cols of a df or a subset
    """
    cols = subset
    if cols is None:
        cols = df.columns
    for col in cols:
        df[col] = df[col].apply(safe_clean_string)
    return df


def reverse_zip_parse(addr):
    """
    this parses an address for a zip code from the right
    """
    global _REVERSE_ZIP_REGEX
    rev = addr[::-1]
    mat = re.search(_REVERSE_ZIP_REGEX, rev)
    if mat:
        return mat[0][::-1]


def nan2none(d):
    """
    recurses through dict changing NaN to None
    """
    for k in d.keys():
        if pd.isna(d[k]):
            d[k] = None
        if type(d[k]) is dict:
            d[k] = nan2none(d[k])
    return d
