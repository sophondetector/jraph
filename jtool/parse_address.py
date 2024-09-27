from typing import Optional

import re
import json

from .utils import reverse_zip_parse, UsStateTools, safe_clean_string, JParse


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
        # _args = [name, street, city, state, country, postalcode]
        # if not any(_args):
        #     raise Exception("bad address")

        self.input = input
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.postalcode = postalcode

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, indent=4)


_name_regex = re.compile(r'^[^\d]+')
_po_box_regex_no_num = re.compile(r'p\.?o\.?\s+box', re.IGNORECASE)
_po_box_regex = re.compile(r'p\.?o\.?\s+box\s+[a-z\-]*\d+', re.IGNORECASE)
_street_term_regex = re.compile(
    r'.*(street|avenue|boulevard|highway|st|ave|av|blvd)[\.,]?',
    re.IGNORECASE
)


def _parse_name(address: str) -> Optional[str]:
    global _name_regex, _po_box_regex
    mat = _name_regex.match(address)
    if mat:
        out = mat.group()
        out = _po_box_regex_no_num.sub('', out).strip()
        return out
    return None


def _parse_street(address: str) -> Optional[str]:
    global _name_regex, _po_box_regex
    pob_mat = _po_box_regex.search(address)
    if pob_mat:
        return pob_mat.group().strip()
    # get rid of name
    stripped = _name_regex.sub('', address).strip()
    mat = _street_term_regex.match(stripped)
    if mat:
        return mat.group()
    return None


def parse_non_us_address(_input) -> ParsedAddress:
    res = ParsedAddress(safe_clean_string(_input))
    res.country = JParse.parse_country(res.input)
    res.city = JParse.parse_city(res.input)
    res.state = JParse.parse_state(res.input)
    res.postalcode = reverse_zip_parse(res.input)
    res.name = _parse_name(res.input)
    res.street = _parse_street(res.input)
    return res


def parse_us_address(_input: Optional[str]) -> ParsedAddress:
    res = ParsedAddress(safe_clean_string(_input))
    res.country = 'usa'
    res.postalcode = reverse_zip_parse(res.input)
    res.state = UsStateTools.parse_state(res.input)
    res.name = _parse_name(res.input)
    res.street = _parse_street(res.input)
    res.city = JParse.parse_city(res.input)
    return res


def _by_whitespace(_input: str) -> list[str]:
    return re.split(r'\s+', _input)


if __name__ == '__main__':
    # import pandas as pd
    # fp = 'world-cities.csv'
    # df = pd.read_csv(fp)
    # import re
    # df.columns
    # df = df.fillna('')

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
