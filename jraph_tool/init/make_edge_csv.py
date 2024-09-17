import pandas as pd

_EDGE_CSV = '~/Public/Datasets/offshore-leaks-db/relationships.csv'
_US_ENTITY_CSV = 'lib/data/init_offshore_data.csv'
_OUTPUT_FP = 'output.csv'


def _load_edge():
    print(f'loading offshore leaks data from {_EDGE_CSV}')
    return pd.read_csv(_EDGE_CSV, index_col=False)


def _load_us_ents():
    print(f'loading offshore leaks data from {_US_ENTITY_CSV}')
    return pd.read_csv(_US_ENTITY_CSV, index_col=False)


def _save_output(df):
    df.to_csv(_OUTPUT_FP, index=False)
    print('save to {} success'.format(_OUTPUT_FP))


def _process(df):
    print('processing dataframe')
    return df


def main(*args, **kwargs):
    return 0


if __name__ == '__main__':
    edge_df = _load_edge()
    use_df = _load_us_ents()
    # out_df = _process(edge_df, use_df)
    # _save_output(out_df)
