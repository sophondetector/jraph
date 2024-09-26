from typing import Optional

import re
import json

from .utils import reverse_zip_parse, UsStateTools


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
_po_box_regex = re.compile(r'p\.?o\.?\s+box\s+\d+', re.IGNORECASE)
_street_term_regex = re.compile(
    r'.*(street|avenue|boulevard|highway|st|ave|av|blvd)[\.,]?')


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


def _parse_country(address: str) -> Optional[str]:
    rev = address[::-1]
    mat = re.match(r'^[^\d]+', rev)
    if mat:
        return mat.group()[::-1]
    return None


def _parse_non_us(_input) -> ParsedAddress:
    res = ParsedAddress(_input)
    res.country = _parse_country(_input)
    res.postalcode = reverse_zip_parse(_input)
    res.name = _parse_name(_input)
    res.street = _parse_street(_input)
    return res


def parse_address(_input: Optional[str], non_us=False) -> ParsedAddress:
    if non_us:
        return _parse_non_us(_input)
    res = ParsedAddress(_input)
    res.country = 'usa'
    res.postalcode = reverse_zip_parse(res.input)
    res.state = UsStateTools.parse_state(res.input)
    res.name = _parse_name(res.input)
    res.street = _parse_street(res.input)
    return res


if __name__ == '__main__':
    import pandas as pd
    df = pd.read_csv('lib/data/us_nodes.csv')
    stop = 20
    for idx, addr in enumerate(df.address):
        if idx == stop:
            break
        res = parse_address(addr)
        print(res)
