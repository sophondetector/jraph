import pandas as pd
from .us_address_parser import UsAddressParser


fp = '~/Public/Datasets/offshore-leaks-db/nodes-addresses.csv'
df = pd.read_csv(fp)
df.fillna('', inplace=True)
df = df[df.apply(lambda r: r.country_codes[:3] == 'USA', axis=1)]
stop = 100
for idx, (nid, row) in enumerate(df.iterrows()):
    if idx == stop:
        break
    res = UsAddressParser.parse(row.address)
    print(res)
print('parse address test done')
