from typing import Optional
from copy import deepcopy

import re
import json

import pandas as pd

from .utils import full2abbr, STATES_ABBR, STATES_FULL, zip2city, zip2state
from .us_city_list import US_CITIES

_REVERSE_ZIP_REGEX = re.compile(r'(\d\d\d\d\-?)? ?(\d\d\d\d\d)')
_USA_REGEX = re.compile(
    r'\b(usa|u s a|united states of america)\b(si)?', re.IGNORECASE)
_NAME_REGEX = re.compile(r'^[^\d]+')
_PO_BOX_REGEX_NO_NUM = re.compile(r'p\.?o\.?\s+box', re.IGNORECASE)
_PO_BOX_REGEX = re.compile(r'p\.?o\.?\s+box\s+[a-z\-]*\d+', re.IGNORECASE)
_STREET_TERM_REGEX = re.compile(
    r'.*(\b|\d+)(street|avenue|boulevard|highway|st|ave?|blvd|court|ct|lane|ln|place|plaza|pl|way|road|rd|terrace|terr|expressway|run|drive|dr|circle|cir)[\.,]?\b',
    re.IGNORECASE
)
_STREET_2_REGEX = re.compile(r'(apt\.?|suite|\#)( ?\#?\d+)', re.IGNORECASE)


# this is for osm geocoder api
class UsAddress:
    def __init__(
        self,
        _input: str,
        name: Optional[str] = None,
        street: Optional[str] = None,
        street_two: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip: Optional[str] = None,
    ):
        self._input = _input
        self.name = name
        self.street = street
        self.street_two = street_two
        self.city = city
        self.state = state
        self.zip = zip
        self.country = 'USA'

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, indent=4)

    def to_dict(self, include_input: bool = True) -> dict:
        res = deepcopy(self.__dict__)
        if include_input:
            return res
        res.pop('_input')
        return res


class UsAddressParser:
    """
    Parse addresses into component parts
    """
    US_CITY_REGEX = re.compile(
        r'\b(' + r'|'.join(US_CITIES) + r')\b',
        re.IGNORECASE
    )

    FULL_US_STATE_REGEX = re.compile(
        r'\b(' + r'|'.join(STATES_FULL) + r')\b',
        re.IGNORECASE
    )

    ABBR_US_STATE_REGEX = re.compile(
        r'\s+(' + '|'.join(STATES_ABBR) + r')\s+',
        re.IGNORECASE
    )

    @classmethod
    def _parse_name(cls, address) -> Optional[str]:
        mat = _NAME_REGEX.match(address)
        if mat:
            out = mat.group()
            out = _PO_BOX_REGEX_NO_NUM.sub('', out).strip()
            if out:
                return out
        return None

    @classmethod
    def _parse_street(cls, address: str) -> Optional[str]:
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
    def _parse_street_two(cls, address: str) -> Optional[str]:
        mat = _STREET_2_REGEX.search(address)
        if mat:
            return mat.group()
        return None

    @classmethod
    def _parse_city(cls, address) -> Optional[str]:
        res = re.split(_REVERSE_ZIP_REGEX, address[::-1], maxsplit=1)
        right = res[-1]
        remainder = right[::-1]
        mat = cls.US_CITY_REGEX.findall(remainder)
        if mat:
            return mat[-1]
        return None

    @classmethod
    def _parse_state(cls, address) -> Optional[str]:
        """tries full, then abbrev, always returns abbreviation"""
        full_res = cls._parse_state_full(address)
        if full_res is not None:
            return full2abbr(full_res)
        abb_res = cls._parse_state_abbr(address)
        if abb_res is None:
            print('couldnt find state in address {}'.format(address))
        return abb_res

    @classmethod
    def _parse_zip(cls, address) -> Optional[str]:
        return cls._reverse_zip_parse(address)

    @classmethod
    def _reverse_zip_parse(cls, addr) -> Optional[str]:
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
        mat = re.search(cls.FULL_US_STATE_REGEX, addr)
        if mat:
            return mat[0].strip()
        return None

    @classmethod
    def _parse_state_abbr(cls, addr) -> Optional[str]:
        mat = re.findall(cls.ABBR_US_STATE_REGEX, addr)
        if mat:
            return mat[-1].strip()
        return None

    @classmethod
    def parse(cls, _input) -> UsAddress:
        output = UsAddress(_input)
        output.zip = cls._parse_zip(_input)

        if output.zip is None:
            output.state = cls._parse_state(_input)
            output.city = cls._parse_city(_input)
        else:
            output.state = zip2state(output.zip)
            output.city = zip2city(output.zip)

        output.street = cls._parse_street(_input)
        output.street_two = cls._parse_street_two(_input)
        output.name = cls._parse_name(_input)
        return output


if __name__ == '__main__':
    fp = '~/Public/Datasets/offshore-leaks-db/nodes-addresses.csv'
    df = pd.read_csv(fp)
    df.fillna('', inplace=True)
    df = df[df.apply(lambda r: 'USA' in r.country_codes, axis=1)]
    stop = 2000
    for idx, (nid, row) in enumerate(df.iterrows()):
        if idx == stop:
            break
        res = UsAddressParser.parse(row.address)
        print(res)
    print('parse address test done')
