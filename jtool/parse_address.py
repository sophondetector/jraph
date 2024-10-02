from typing import Optional

import re
import json

import pandas as pd

_REVERSE_ZIP_REGEX = re.compile(r'(\d\d\d\d\-?)? ?(\d\d\d\d\d)')
_USA_REGEX = re.compile(
    r'\b(usa|u s a|united states of america)\b(si)?', re.IGNORECASE)
_NAME_REGEX = re.compile(r'^[^\d]+')
_PO_BOX_REGEX_NO_NUM = re.compile(r'p\.?o\.?\s+box', re.IGNORECASE)
_PO_BOX_REGEX = re.compile(r'p\.?o\.?\s+box\s+[a-z\-]*\d+', re.IGNORECASE)
_STREET_TERM_REGEX = re.compile(
    r'.*(street|avenue|boulevard|highway|st|ave?|blvd)[\.,]?',
    re.IGNORECASE
)


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

_FULL2ABBR_MAP = {full: abbr for full, abbr in _US_STATE_TUPLES}
_ABBR2FULL_MAP = {abbr: full for full, abbr in _US_STATE_TUPLES}


def full2abbr(full): return _FULL2ABBR_MAP.get(full)
def abbr2full(abbr): return _ABBR2FULL_MAP.get(abbr)


# this is for osm geocoder api
class ParsedAddress:
    def __init__(
        self,
        input: str,
        name: Optional[str] = None,
        street: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        postalcode: Optional[str] = None,
    ):
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.postalcode = postalcode

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, indent=4)


class AddressParser:
    """
    Parse addresses into component parts
    """
    _fp = 'lib/data/country_subcountry_city.csv'
    _city_col = 'name'
    _country_col = 'country'
    _country_code_col = 'country_code'
    _state_col = 'subcountry'
    _geonameid = '_geonameid'
    _df = pd.read_csv(_fp)
    _df.fillna('', inplace=True)

    countries = _df[_country_col].unique()

    all_cities = _df[_city_col].unique()
    us_cities = _df.loc[_df[_country_code_col] == 'USA'][_city_col]
    non_us_cities = _df.loc[_df[_country_code_col] != 'USA'][_city_col]

    states_us_full = [full for full, abbr in _US_STATE_TUPLES]
    states_us_abbr = [abbr for full, abbr in _US_STATE_TUPLES]
    states_non_us = _df.loc[_df[_country_code_col] != 'USA'].as_list()

    # def _make_regex(list_of_strings) -> re.Pattern:
    #     return re.compile(
    #         r'\b(' + r'|'.join(list_of_strings) + r')\b',
    #         re.IGNORECASE
    #     )
    # US_CITY_REGEX = _make_regex(us_cities)

    US_CITY_REGEX = re.compile(
        r'\b(' + r'|'.join(us_cities) + r')\b',
        re.IGNORECASE
    )

    # TODO make per country/state
    NON_US_CITY_REGEX = re.compile(
        r'\b(' + r'|'.join(non_us_cities) + r')\b',
        re.IGNORECASE
    )

    FULL_US_STATE_REGEX = re.compile(
        r'\b(' + r'|'.join(states_us_full) + r')\b',
        re.IGNORECASE
    )

    ABBR_US_STATE_REGEX = re.compile(
        r'\s+(' + '|'.join(states_us_abbr) + r')\s+',
        re.IGNORECASE
    )

    NON_US_STATE_REGEX = re.compile(
        r'\s+(' + '|'.join(states_non_us) + r')\s+',
        re.IGNORECASE
    )

    @classmethod
    def parse_name(cls, address) -> Optional[str]:
        mat = _NAME_REGEX.match(address)
        if mat:
            out = mat.group()
            out = _PO_BOX_REGEX_NO_NUM.sub('', out).strip()
            if out:
                return out
        return None

    @classmethod
    def parse_street(cls, address: str) -> Optional[str]:
        pob_mat = _PO_BOX_REGEX.search(address)
        if pob_mat:
            return pob_mat.group().strip()
        # get rid of name
        stripped = _NAME_REGEX.sub('', address).strip()
        mat = _STREET_TERM_REGEX.match(stripped)
        if mat:
            return mat.group()
        return None

    @classmethod
    def parse_city(cls, address) -> Optional[str]:
        raise NotImplementedError()

    @classmethod
    def parse_country(cls, address) -> Optional[str]:
        raise NotImplementedError()

    @classmethod
    def parse_state(cls, address) -> Optional[str]:
        """tries full, then abbrev, always returns abbreviation"""
        full_res = cls._parse_state_full(address)
        if full_res is not None:
            return cls.full2abbr(full_res)
        abb_res = cls._parse_state_abbr(address)
        if abb_res is None:
            print('couldnt find state in address {}'.format(address))
        return abb_res

    @classmethod
    def parse_zip(cls, address) -> Optional[str]:
        return cls._reverse_zip_parse(address)

    @classmethod
    def _reverse_zip_parse(addr) -> Optional[str]:
        """
        this parses an address for a zip code from the right
        """
        rev = addr[::-1]
        mat = re.search(_REVERSE_ZIP_REGEX, rev)
        if mat:
            return mat[0][::-1]
        return None

    @classmethod
    def _parse_state_full(cls, addr) -> Optional[str]:
        mat = re.search(cls._FULL_STATE_REGEX, addr)
        if mat:
            return mat[0].strip()
        return None

    @classmethod
    def _parse_state_abbr(cls, addr) -> Optional[str]:
        mat = re.search(cls._ABBR_STATE_REGEX, addr)
        if mat:
            return mat[0].strip()
        return None


if __name__ == '__main__':
    import pandas as pd
    fp = '~/Public/Datasets/offshore-leaks-db/nodes-addresses.csv'
    df = pd.read_csv(fp)
    df.fillna('', inplace=True)
    stop = 2000
    for idx, (nid, row) in enumerate(df.iterrows()):
        if idx == stop:
            break
        if 'USA' in row.country_codes:
            print(parse_us_address(row.address))
            continue
        print(parse_non_us_address(row.address))
    print('parse address done')
