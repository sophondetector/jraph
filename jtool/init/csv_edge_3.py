import pandas as pd

EDGE_CSV = '~/Public/Datasets/offshore-leaks-db/relationships.csv'
US_ENTITY_CSV = 'lib/data/init_offshore_data.csv'
OUTPUT_FP = 'lib/data/init_offshore_edges.csv'


def _load_us_edges():
    print(f'loading offshore leaks data from {EDGE_CSV}')
    return pd.read_csv(OUTPUT_FP, index_col=False)


def _load_edge():
    print(f'loading offshore leaks data from {EDGE_CSV}')
    return pd.read_csv(EDGE_CSV, index_col=False)


def _load_us_ents():
    print(f'loading offshore leaks data from {US_ENTITY_CSV}')
    return pd.read_csv(US_ENTITY_CSV, index_col=False)


def _save_output(df):
    df.to_csv(OUTPUT_FP, index=False)
    print('save to {} success'.format(OUTPUT_FP))


if __name__ == '__main__':
    print('loading edge and us entity csvs')
    edge_df = _load_edge()
    use_df = _load_us_ents()

    print('merging and us entity csvs')
    start_in_us = edge_df.merge(
        use_df['node_id'], how='inner',
        left_on='_start', right_on='node_id'
    )
    end_in_us = edge_df.merge(
        use_df['node_id'], how='inner',
        left_on='_end', right_on='node_id'
    )

    out = pd.concat([start_in_us, end_in_us])
    out.drop('node_id', axis=1, inplace=True)
    out.drop_duplicates(inplace=True)

    _save_output(out)
