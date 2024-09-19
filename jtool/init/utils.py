import re
import pandas as pd

states = [
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

SPACE_REGEX = re.compile(r'\s\s+')
USA_REGEX = re.compile(r' ?(usa|u s a|united states of america)( si)?')


_REMOVE_TO_CLEAN_REGEX = re.compile(r'[^a-z0-9 ]')


def safe_clean_string(s):
    """
    ensures input is a string before proceeding
    if its not a string just returns input
    """
    if type(s) is not str:
        return s
    s = re.sub(SPACE_REGEX, ' ', s)
    return re.sub(_REMOVE_TO_CLEAN_REGEX, '', s.lower())


def clean_all_strings(df, subset=None):
    """
    runs safe_clean_string on all cols of a df or a subset
    """
    cols = subset
    if cols is None:
        cols = df.columns
    for col in cols:
        df[col] = df[col].apply(safe_clean_string)
    return df


def parse_full_state(addr):
    mat = re.search(_STATE_REGEX, addr.lower())
    if mat:
        return mat[0].strip()


_REVERSE_ZIP_REGEX = re.compile(r'(\d\d\d\d\-?)? ?(\d\d\d\d\d)')
_STATE_REGEX = re.compile(
    ' +(' + '|'.join(full for full, abb in states) + ') +'
)
_STATE_ABBREV_REGEX = re.compile(
    ' +(' + '|'.join(abb for full, abb in states) + ') +'
)

_FULL_2_ABBREV_MAP = {full: short for full, short in states}
def full2abbrev(state): return _FULL_2_ABBREV_MAP.get(state)


_ABBREV_2_FULL_MAP = {abb: full for full, abb in states}
def abbrev2full(state): return _ABBREV_2_FULL_MAP.get(state)


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


TEST_NODES = [
    {"node_id": 1, "properties": {"name": "foo", "type": "corp"}},
    {"node_id": 2, "properties": {"name": "bar", "type": "corp"}},
    {"node_id": 3, "properties": {"name": "bing", "type": "corp"}},
    {"node_id": 4, "properties": {"name": "boing", "type": "corp"}}
]
