import pandas as pd
import jtool.utils as dbh

RAW_CSV_FP = 'nodes-entities.csv'
OUTPUT_FP = 'output.csv'
STATE_COORD_CSV_FP = 'lib/data/state_lat_long.csv'

RAW_ADDR_COL = 'address'
RAW_COUNTRY_CODES_COL = 'country_codes'
RAW_NAME_COL = 'name'
FULL_STATE_COL = 'state'
ABBREV_STATE_COL = 'state_abbr'
ZIP_COL = 'zip'
ZIP_FIVE_COL = 'zip_five'


def _add_coords(idf):
    scdf = pd.read_csv(STATE_COORD_CSV_FP, index_col=None)
    return idf.merge(scdf, how='inner',
                     left_on=FULL_STATE_COL, right_on='state_full')


def _process(df):
    non_opt = [RAW_ADDR_COL, RAW_COUNTRY_CODES_COL, RAW_NAME_COL]
    df.dropna(
        subset=non_opt,
        inplace=True)
    # limit to us
    df = df[df[RAW_COUNTRY_CODES_COL].apply(lambda cc: 'USA' in cc)]
    # parse zips
    df[ZIP_COL] = df[RAW_ADDR_COL].apply(dbh.reverse_zip_parse)
    df.dropna(subset=[ZIP_COL], inplace=True)
    df[ZIP_FIVE_COL] = df[ZIP_COL].apply(lambda s: s[:5])
    # clean all strings
    df = dbh.clean_all_strings(df)
    # parse state
    df[FULL_STATE_COL] = df[RAW_ADDR_COL].apply(dbh.parse_full_state)
    df.dropna(subset=[FULL_STATE_COL], inplace=True)
    df = _add_coords(df)
    return df


def main():
    print(f'loading offshore leaks data from {RAW_CSV_FP}')
    df = pd.read_csv(RAW_CSV_FP, index_col=False)
    print('processing dataframe')
    df = _process(df)
    df.to_csv(OUTPUT_FP, index=False)
    print('save to {} success'.format(OUTPUT_FP))

    return 0


if __name__ == '_main_':
    main()
