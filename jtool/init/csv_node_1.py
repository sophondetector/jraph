import pandas as pd
import jtool.init_scripts.init_db_helpers as dbh

_RAW_CSV_FP = 'nodes-entities.csv'
_OUTPUT_FP = 'output.csv'
_STATE_COORD_CSV_FP = 'lib/data/state_lat_long.csv'

_RAW_ADDR_COL = 'address'
_RAW_COUNTRY_CODES_COL = 'country_codes'
_RAW_NAME_COL = 'name'
_FULL_STATE_COL = 'state'
_ABBREV_STATE_COL = 'state_abbr'
_ZIP_COL = 'zip'
_ZIP_FIVE_COL = 'zip_five'


def _add_coords(idf):
    scdf = pd.read_csv(_STATE_COORD_CSV_FP, index_col=None)
    return idf.merge(scdf, how='inner',
                     left_on=_FULL_STATE_COL, right_on='state_full')


def _process(df):
    non_opt = [_RAW_ADDR_COL, _RAW_COUNTRY_CODES_COL, _RAW_NAME_COL]
    df.dropna(
        subset=non_opt,
        inplace=True)
    # limit to us
    df = df[df[_RAW_COUNTRY_CODES_COL].apply(lambda cc: 'USA' in cc)]
    # parse zips
    df[_ZIP_COL] = df[_RAW_ADDR_COL].apply(dbh.reverse_zip_parse)
    df.dropna(subset=[_ZIP_COL], inplace=True)
    df[_ZIP_FIVE_COL] = df[_ZIP_COL].apply(lambda s: s[:5])
    # clean all strings
    df = dbh.clean_all_strings(df)
    # parse state
    df[_FULL_STATE_COL] = df[_RAW_ADDR_COL].apply(dbh.parse_full_state)
    df.dropna(subset=[_FULL_STATE_COL], inplace=True)
    df = _add_coords(df)
    return df


def main():
    print(f'loading offshore leaks data from {_RAW_CSV_FP}')
    df = pd.read_csv(_RAW_CSV_FP, index_col=False)
    print('processing dataframe')
    df = _process(df)
    df.to_csv(_OUTPUT_FP, index=False)
    print('save to {} success'.format(_OUTPUT_FP))

    return 0


if __name__ == '__main__':
    main()
