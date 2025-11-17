# import re
#
# import pandas as pd
#
#
# _SPACE_REGEX = re.compile(r'\s\s+')
# _REMOVE_TO_CLEAN_REGEX = re.compile(r'[^a-z0-9 ]')
#
#
# class DataLoaders:
#     class GIS:
#         def zipcodes(self):
#             return pd.read_csv('~/Public/Datasets/GIS/zipcodes.csv')
#
#         def world_cities(self):
#             return pd.read_csv('~/Public/Datasets/GIS/world-cities.csv')
#
#         def country_info(self):
#             return pd.read_csv('~/Public/Datasets/GIS/country_information.csv')
#
#     class OffshoreLeaks:
#         base = '~/Public/Datasets/offshore-leaks-db/'
#
#         @classmethod
#         def entities(cls):
#             return pd.read_csv(cls.base + 'nodes-entities.csv')
#
#         @classmethod
#         def addresses(cls):
#             return pd.read_csv(cls.base + 'nodes-addresses.csv')
#
#         @classmethod
#         def officers(cls):
#             return pd.read_csv(cls.base + 'nodes-officers.csv')
#
#         @classmethod
#         def others(cls):
#             return pd.read_csv(cls.base + 'nodes-others.csv')
#
#         @classmethod
#         def itermediaries(cls):
#             return pd.read_csv(cls.base + 'nodes-intermediaries.csv')
#
#         @classmethod
#         def relationships(cls):
#             return pd.read_csv(cls.base + 'relationships.csv')
#
#
# def safe_clean_string(s):
#     """
#     ensures input is a string before proceeding
#     if its not a string just returns input
#     """
#     if type(s) is not str:
#         return s
#     s = re.sub(_SPACE_REGEX, ' ', s)
#     return re.sub(_REMOVE_TO_CLEAN_REGEX, '', s.lower())
#
#
# def clean_dataframe_strings(df, subset=None):
#     """
#     runs safe_clean_string on all cols of a df or a subset
#     """
#     cols = subset
#     if cols is None:
#         cols = df.columns
#     for col in cols:
#         df[col] = df[col].apply(safe_clean_string)
#     return df
#

def nan2none(d: dict) -> dict:
    """
    recurses through dict changing NaN to None
    """
    for k in d.keys():
        if pd.isna(d[k]):
            d[k] = None
        if type(d[k]) is dict:
            d[k] = nan2none(d[k])
    return d

#
# def split_by_whitespace(_input: str) -> list[str]:
#     return re.split(r'\s+', _input)
#
#
# OFFSHORE_LEAKS_COLUMNS = [
#     "name",
#     "lat",
#     "long",
#     "node_id",
#     "address",
#     "_id",
#     "original_name",
#     "former_name",
#     "jurisdiction",
#     "jurisdiction_description",
#     "company_type",
#     "internal_id",
#     "incorporation_date",
#     "inactivation_date",
#     "struck_off_date",
#     "dorm_date",
#     "status",
#     "service_provider",
#     "ibcRUC",
#     "country_codes",
#     "countries",
#     "sourceID",
#     "valid_until",
#     "note",
#     "zip",
#     "zip_five",
#     "state"
# ]
